import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Module 1: ROS 2 Fundamentals',
    Svg: require('../../static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Learn the fundamentals of Robot Operating System 2 (ROS 2), including architecture,
        nodes, topics, services, and actions. Master the core concepts that power modern robotics applications.
      </>
    ),
  },
  {
    title: 'Module 2: Gazebo/Unity Simulation',
    Svg: require('../../static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Explore physics simulation with Gazebo and Unity integration for robotics.
        Learn simulation-to-reality transfer techniques and domain randomization methods.
      </>
    ),
  },
  {
    title: 'Module 3: NVIDIA Isaac Platform',
    Svg: require('../../static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Discover the NVIDIA Isaac platform for robotics development. Learn about Isaac Sim,
        Isaac ROS, and optimization techniques for AI-powered robots.
      </>
    ),
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA) Models',
    Svg: require('../../static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Master Vision-Language-Action models for embodied AI. Learn about RT-1, BC-Z,
        OpenVLA, and how to deploy multimodal models on robots.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
