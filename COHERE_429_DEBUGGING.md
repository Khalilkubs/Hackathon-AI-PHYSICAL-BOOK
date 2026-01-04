# Understanding Cohere API 429 Errors with New Account

## Problem Description
You are experiencing HTTP 429 "Too Many Requests" errors when using the Cohere API, even though you have a new account with first-time use. This document explains why this might happen and how to resolve it.

## Why 429 Errors Can Occur with New Accounts

### 1. Trial Account Limits
- **Cohere trial accounts** often have lower rate limits than expected
- Even new accounts may have restrictions like 10-50 requests per minute
- Free tier accounts typically have strict usage limits

### 2. Account Verification Status
- New accounts may need email verification before full access
- Some regions may have additional verification requirements
- Account status might be pending review

### 3. Geographic Restrictions
- Cohere may have regional rate limiting
- Some countries/regions have different access levels
- IP-based restrictions might apply

### 4. Model-Specific Limits
- Some embedding models (like `embed-multilingual-v2.0`) might have different rate limits
- Deprecated or older models might have limited access

### 5. Soft Rate Limits
- Even with new accounts, there might be "soft" limits that trigger 429s
- These are not the same as hard rate limits but serve to prevent abuse

## How Our System Handles This Now

### Enhanced Error Logging
- The system now provides more specific error messages
- Distinguishes between actual rate limiting and other issues
- Includes detailed error information for debugging

### Retry Logic with Exponential Backoff
- The system now implements smart retry logic
- Uses exponential backoff with jitter to avoid repeated failures
- Automatically retries on 429 and network errors

## Steps to Resolve

### 1. Verify Your Account Status
- Log into your Cohere dashboard
- Check if your account is fully verified
- Confirm your subscription tier and limits

### 2. Check Your API Key
- Ensure the API key in your `.env` file is correct
- Verify the key has the right permissions
- Consider regenerating the key if needed

### 3. Monitor Your Usage
- Check your Cohere dashboard for usage statistics
- See if you're hitting any soft or hard limits
- Note the time of day when errors occur

### 4. Try Alternative Models
- Consider using `embed-english-v3.0` instead of `embed-multilingual-v2.0`
- Different models may have different rate limits

### 5. Contact Cohere Support
- If you're certain your account is new and limits seem too restrictive
- Cohere support can provide specific information about your account limits

## Testing the System

After implementing the changes, you can test with:

```bash
python retrieve.py "What are the fundamentals of ROS 2?" --top-k 3
```

The system will now:
1. Show detailed error messages if 429 occurs
2. Automatically retry failed requests with backoff
3. Provide specific guidance about non-rate-limiting causes

## Important Notes

- The enhanced error messages specifically indicate when it's likely NOT a rate limiting issue
- New accounts may have unexpected restrictions despite being "new"
- The system now handles 429 errors more gracefully with retries
- Check your Cohere dashboard for actual usage metrics to confirm if it's truly rate limiting