#!/usr/bin/env python3
"""
RAG Retrieval Validation System
Validate stored embeddings in Qdrant by performing similarity searches and validating results.
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

# Import required libraries
try:
    import openai
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required dependencies using: pip install -r requirements.txt")
    sys.exit(1)


import time
import random

class QueryEmbedder:
    """Implements query embedding generation using OpenAI API"""

    def __init__(self, api_key: str, model: str = "text-embedding-3-small", max_retries: int = 3, base_delay: float = 1.0):
        """
        Initialize the query embedder
        Uses text-embedding-3-small which produces 1536-dimensional vectors to match existing embeddings
        """
        self.api_key = api_key
        # Check if it's an OpenRouter key (starts with "sk-or-")
        if api_key.startswith("sk-or-"):
            # Use OpenRouter's API endpoint with a separate client to avoid conflicts
            from openai import OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"  # Use OpenRouter's API endpoint
            )
        else:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)

        self.model = model
        self.max_retries = max_retries
        self.base_delay = base_delay  # Base delay in seconds for exponential backoff

    def _exponential_backoff_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter"""
        delay = self.base_delay * (2 ** attempt)  # Exponential backoff
        jitter = random.uniform(0, delay * 0.1)  # Add up to 10% jitter
        return delay + jitter

    def embed_query(self, query_text: str) -> Optional[List[float]]:
        """
        Generate embedding for a query string with retry logic
        """
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.embeddings.create(
                    input=[query_text],
                    model=self.model
                )

                # Handle response based on whether it's OpenAI or OpenRouter format
                if hasattr(response, 'data') and response.data and len(response.data) > 0:
                    # Standard OpenAI format
                    embedding = response.data[0].embedding
                elif isinstance(response, dict) and 'data' in response and response['data']:
                    # OpenRouter format (may return dict)
                    embedding = response['data'][0]['embedding']
                elif hasattr(response, '__dict__') and 'data' in response.__dict__:
                    # Alternative object format
                    data_list = response.data if isinstance(response.data, list) else getattr(response, 'data', [])
                    if data_list:
                        embedding = data_list[0].embedding if hasattr(data_list[0], 'embedding') else data_list[0]['embedding']
                    else:
                        logger.error("No embeddings returned from API for query")
                        return None
                else:
                    logger.error("Unexpected response format from API")
                    return None

                if embedding and len(embedding) > 0:
                    logger.debug(f"Generated query embedding with {len(embedding)} dimensions")
                    return embedding
                else:
                    logger.error("No embeddings returned from API for query")
                    return None

            except Exception as e:
                error_msg = str(e)
                error_type = type(e).__name__

                if attempt < self.max_retries:
                    # Check if this is a retryable error (429, 5xx, network issues)
                    is_retryable = ("rate_limit" in error_msg.lower() or
                                  "429" in error_msg or
                                  "Too Many Requests" in error_msg or
                                  "50" in error_msg or  # 5xx server errors
                                  "Connection" in error_msg or
                                  "timeout" in error_msg.lower() or
                                  "network" in error_msg.lower())

                    if is_retryable:
                        delay = self._exponential_backoff_delay(attempt)
                        logger.warning(f"Attempt {attempt + 1} failed with {error_type}: {e}. Retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue  # Retry
                    else:
                        # Non-retryable error, fail immediately
                        logger.error(f"Non-retryable error with OpenAI API - {error_type}: {e}")
                        logger.error(f"Full error details: {repr(e)}")
                        return None
                else:
                    # Final attempt failed
                    if "401" in error_msg or "Unauthorized" in error_msg:
                        logger.error(f"Authentication error with OpenAI API (check your API key): {e}")
                    elif "429" in error_msg or "Too Many Requests" in error_msg or "rate_limit" in error_msg.lower():
                        logger.error(f"HTTP 429 error with OpenAI API - {error_type}: {e}")
                        logger.error("This could be due to rate limiting, account restrictions, or other API issues.")
                        logger.error("Please check your OpenAI account status, usage limits, and API key validity.")
                    elif "403" in error_msg or "Forbidden" in error_msg:
                        logger.error(f"HTTP 403 error with OpenAI API - {error_type}: {e}")
                        logger.error("Access forbidden - check API key permissions and account status.")
                    elif "400" in error_msg or "Bad Request" in error_msg:
                        logger.error(f"HTTP 400 error with OpenAI API - {error_type}: {e}")
                        logger.error("Bad request - check query format, model name, and input parameters.")
                    else:
                        logger.error(f"Error when generating query embedding - {error_type}: {e}")
                        logger.error(f"Full error details: {repr(e)}")
                    return None


class QdrantConnector:
    """Implements Qdrant connector class to establish connection and validate collection"""

    def __init__(self, config: dict):
        self.config = config
        self.client = QdrantClient(
            url=config['qdrant_url'],
            api_key=config['qdrant_api_key']
        )
        self.collection_name = config['qdrant_collection_name']

    def validate_connection(self) -> bool:
        """Validate Qdrant connection and collection availability"""
        try:
            # Try to get collection info to verify connection
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Successfully connected to Qdrant collection: {self.collection_name}")
            logger.info(f"Collection vector size: {collection_info.config.params.vectors.size}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            return False

    def get_vector_size(self) -> Optional[int]:
        """Get the vector size of the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.config.params.vectors.size
        except Exception as e:
            logger.error(f"Failed to get vector size: {e}")
            return None

    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Perform similarity search in Qdrant to retrieve top-k results"""
        try:
            # Attempt search without strict dimension validation
            # Qdrant can handle some dimension mismatches depending on configuration
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            # Format results according to the original storage module's approach
            formatted_results = []
            for hit in search_results:
                result = {
                    "chunk_id": hit.payload.get("chunk_id", ""),
                    "similarity_score": hit.score,
                    "content": hit.payload.get("content", ""),  # This field may be empty if not stored
                    "source_url": hit.payload.get("source_url", ""),
                    "document_title": hit.payload.get("document_title", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0)
                }
                formatted_results.append(result)

            logger.info(f"Search returned {len(formatted_results)} results")
            return formatted_results
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []


class Query:
    """Represents a user search query that will be converted to an embedding for similarity search"""

    def __init__(self, text: str, embedding: Optional[List[float]] = None):
        self.text = text
        self.embedding = embedding
        self.created_at = datetime.now()

    def validate(self):
        """Validate the query"""
        if not self.text or not self.text.strip():
            raise ValueError("Query text cannot be empty")
        if self.embedding is not None and len(self.embedding) == 0:
            raise ValueError("Query embedding cannot be empty")


class RetrievalResult:
    """Contains relevant text chunks, similarity scores, source URLs, and metadata returned from the vector search"""

    def __init__(self, chunk_id: str, similarity_score: float, content: str,
                 source_url: str, document_title: str, chunk_index: int, metadata: Dict[str, Any]):
        self.chunk_id = chunk_id
        self.similarity_score = similarity_score
        self.content = content
        self.source_url = source_url
        self.document_title = document_title
        self.chunk_index = chunk_index
        self.metadata = metadata

    def validate(self):
        """Validate the retrieval result"""
        if not self.chunk_id:
            raise ValueError("Chunk ID cannot be empty")
        if not 0.0 <= self.similarity_score <= 1.0:
            raise ValueError("Similarity score must be between 0.0 and 1.0")
        if not self.content:
            raise ValueError("Content cannot be empty")
        if not self.source_url:
            raise ValueError("Source URL cannot be empty")


class ResultValidator:
    """Validates retrieved results against source URLs and metadata"""

    def __init__(self, similarity_threshold: float = 0.5):
        self.similarity_threshold = similarity_threshold

    def validate_results(self, query: str, search_results: List[Dict]) -> 'ValidationReport':
        """Validate retrieved results and generate validation report"""
        report = ValidationReport(query)

        if not search_results:
            report.validation_passed = False
            report.error_message = "No results returned from search"
            return report

        report.results_count = len(search_results)

        # Calculate similarity statistics
        similarity_scores = [result['similarity_score'] for result in search_results]
        report.avg_similarity_score = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
        report.min_similarity_score = min(similarity_scores) if similarity_scores else 0
        report.max_similarity_score = max(similarity_scores) if similarity_scores else 0

        # Validate each result and assess relevance
        valid_results_count = 0
        relevance_score_sum = 0

        for result in search_results:
            is_valid = True
            relevance_issues = []

            # Check if similarity score meets threshold
            if result['similarity_score'] < self.similarity_threshold:
                is_valid = False
                relevance_issues.append('Similarity score below threshold')
                report.validation_details.append({
                    'chunk_id': result['chunk_id'],
                    'issue': 'Similarity score below threshold',
                    'score': result['similarity_score'],
                    'threshold': self.similarity_threshold
                })
            else:
                # Add to relevance score if above threshold
                relevance_score_sum += result['similarity_score']

            # Check if source URL is present and valid (but don't fail validation if missing)
            if result['source_url'] and result['source_url'].strip() != "":
                report.source_urls_matched += 1
            else:
                relevance_issues.append('Missing or empty source URL')
                report.validation_details.append({
                    'chunk_id': result['chunk_id'],
                    'issue': 'Missing or empty source URL'
                })

            # Check if content is present (but don't fail validation if missing)
            if result['content'] and result['content'].strip() != "":
                # Assess content relevance based on query terms only if content exists
                query_lower = query.lower()
                content_lower = result['content'].lower()
                query_terms = set(query_lower.split())
                content_terms = set(content_lower.split())

                # Calculate overlap between query and content terms
                if query_terms and content_terms:
                    term_overlap = len(query_terms.intersection(content_terms))
                    term_ratio = term_overlap / len(query_terms)

                    # If less than 10% of query terms appear in content, flag as potentially irrelevant
                    if term_ratio < 0.1:
                        relevance_issues.append(f'Low content relevance (only {term_ratio:.1%} query terms matched)')
                        report.validation_details.append({
                            'chunk_id': result['chunk_id'],
                            'issue': f'Low content relevance (only {term_ratio:.1%} query terms matched)',
                            'query_terms_matched': term_overlap,
                            'total_query_terms': len(query_terms)
                        })
            else:
                relevance_issues.append('Missing or empty content')
                report.validation_details.append({
                    'chunk_id': result['chunk_id'],
                    'issue': 'Missing or empty content'
                })

            # Check if metadata is present and valid
            if 'metadata' in result and result['metadata']:
                report.metadata_validated += 1
            else:
                relevance_issues.append('Missing metadata')
                report.validation_details.append({
                    'chunk_id': result['chunk_id'],
                    'issue': 'Missing metadata'
                })

            # For validation purposes, only similarity score is critical for validity
            # Other issues are logged but don't necessarily make the result invalid
            if result['similarity_score'] >= self.similarity_threshold:
                valid_results_count += 1

        # Determine if overall validation passes
        # Consider validation passed if at least one result meets similarity threshold
        # since the main goal is to verify that the search returns relevant results
        report.validation_passed = valid_results_count > 0

        # Calculate average relevance score
        if valid_results_count > 0:
            report.avg_relevance_score = relevance_score_sum / valid_results_count
        else:
            report.avg_relevance_score = 0

        logger.info(f"Validation completed: {valid_results_count}/{len(search_results)} results passed")
        return report


class ValidationReport:
    """Summarizes the results of retrieval tests, including relevance metrics and error status"""

    def __init__(self, query: str):
        self.query = query
        self.timestamp = datetime.now()
        self.results_count = 0
        self.validation_passed = False
        self.validation_details = []
        self.source_urls_matched = 0
        self.metadata_validated = 0
        self.avg_similarity_score = 0.0
        self.min_similarity_score = 0.0
        self.max_similarity_score = 0.0
        self.avg_relevance_score = 0.0  # New field for relevance assessment
        self.error_message = ""

    def validate(self):
        """Validate the validation report"""
        if not self.query:
            raise ValueError("Query cannot be empty")
        if self.results_count < 0:
            raise ValueError("Results count cannot be negative")


def load_config():
    """Load and validate configuration from environment variables"""
    config = {
        'openai_api_key': os.getenv('OPENROUTER_API_KEY') or os.getenv('OPEN_API_KEY'),
        'qdrant_url': os.getenv('QDRANT_URL'),
        'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
        'qdrant_collection_name': os.getenv('QDRANT_COLLECTION_NAME', 'document_embeddings'),
        'default_top_k': int(os.getenv('DEFAULT_TOP_K', 5)),
        'similarity_threshold': float(os.getenv('SIMILARITY_THRESHOLD', 0.5)),
    }

    # Validate required environment variables
    required_vars = ['openai_api_key', 'qdrant_url', 'qdrant_api_key']
    missing_vars = [var for var in required_vars if not config[var]]

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Additional validation
    if config['default_top_k'] <= 0:
        raise ValueError("DEFAULT_TOP_K must be a positive integer")

    if not 0.0 <= config['similarity_threshold'] <= 1.0:
        raise ValueError("SIMILARITY_THRESHOLD must be between 0.0 and 1.0")

    logger.info(f"Configuration loaded successfully. Collection: {config['qdrant_collection_name']}")
    return config


def validate_qdrant_connection(config: dict) -> bool:
    """Validate Qdrant connection and collection availability (wrapper function)"""
    connector = QdrantConnector(config)
    return connector.validate_connection()


def main():
    """Main function with command-line interface - implements end-to-end query processing"""
    parser = argparse.ArgumentParser(
        description="RAG Retrieval Validation System - Validate stored embeddings in Qdrant"
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='Query text to search for similar content'
    )
    parser.add_argument(
        '--top-k',
        type=int,
        default=5,
        help='Number of results to retrieve (default: 5)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=None,
        help='Minimum similarity score threshold (default: from config)'
    )
    parser.add_argument(
        '--queries-file',
        type=str,
        help='Path to file containing multiple queries (one per line)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        config = load_config()
        logger.info("Configuration loaded successfully")

        # Validate Qdrant connection
        if not validate_qdrant_connection(config):
            logger.error("Failed to connect to Qdrant. Please check your configuration.")
            sys.exit(1)

        # Handle multiple queries from file or single query
        queries = []
        if args.queries_file:
            if not os.path.exists(args.queries_file):
                logger.error(f"Queries file does not exist: {args.queries_file}")
                sys.exit(1)

            with open(args.queries_file, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]

            if not queries:
                logger.error(f"No queries found in file: {args.queries_file}")
                sys.exit(1)

            logger.info(f"Loaded {len(queries)} queries from {args.queries_file}")
        elif not args.query:
            print("Please provide a query to search for similar content or use --queries-file for multiple queries.")
            parser.print_help()
            sys.exit(1)
        else:
            queries = [args.query]

        # Use configurable threshold (command line arg overrides config)
        threshold = args.threshold if args.threshold is not None else config['similarity_threshold']

        # Create components
        qdrant_connector = QdrantConnector(config)
        query_embedder = QueryEmbedder(
            config['openai_api_key'],
            max_retries=3,  # Number of retry attempts
            base_delay=1.0  # Base delay in seconds for exponential backoff
        )
        result_validator = ResultValidator(threshold)

        # Process queries
        for i, query in enumerate(queries, 1):
            if len(queries) > 1:
                print(f"\n--- Processing Query {i}/{len(queries)} ---")

            print(f"Query: {query}")
            print(f"Searching for top {args.top_k} similar results...")

            # Generate embedding for the query
            logger.info("Generating embedding for query...")
            query_embedding = query_embedder.embed_query(query)
            if not query_embedding:
                logger.error(f"Failed to generate embedding for query: {query}")
                continue

            # Perform similarity search
            logger.info(f"Performing similarity search for top {args.top_k} results...")
            search_results = qdrant_connector.search_similar(query_embedding, args.top_k)

            if not search_results:
                logger.warning("No results returned from search")
                continue

            # Validate results
            logger.info("Validating results...")
            validation_report = result_validator.validate_results(query, search_results)

            # Display results
            print(f"\n--- Search Results for Query: '{query}' ---")
            print(f"Total results: {validation_report.results_count}")
            print(f"Average similarity score: {validation_report.avg_similarity_score:.3f}")
            print(f"Average relevance score: {validation_report.avg_relevance_score:.3f}")
            print(f"Min similarity score: {validation_report.min_similarity_score:.3f}")
            print(f"Max similarity score: {validation_report.max_similarity_score:.3f}")
            print(f"Source URLs matched: {validation_report.source_urls_matched}/{validation_report.results_count}")
            print(f"Metadata validated: {validation_report.metadata_validated}/{validation_report.results_count}")
            print(f"Validation passed: {validation_report.validation_passed}")

            if validation_report.error_message:
                print(f"Error: {validation_report.error_message}")

            if validation_report.validation_details:
                print(f"Validation issues found: {len(validation_report.validation_details)}")
                for detail in validation_report.validation_details[:3]:  # Show first 3 issues
                    print(f"  - {detail.get('chunk_id', 'N/A')}: {detail.get('issue', 'Unknown')}")
                if len(validation_report.validation_details) > 3:
                    print(f"  ... and {len(validation_report.validation_details) - 3} more issues")

            print(f"\n--- Top {min(3, len(search_results))} Results ---")
            for j, result in enumerate(search_results[:3], 1):
                print(f"\n{j}. [Score: {result['similarity_score']:.3f}] Source: {result['source_url']}")
                print(f"   Content: {result['content'][:200]}{'...' if len(result['content']) > 200 else ''}")
                print(f"   Document: {result['document_title']}")

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        sys.exit(1)


# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    main()