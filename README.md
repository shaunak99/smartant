# Ant Exploration using RL

This repository showcases a Reinforcement Learning agent using [NEAT-python](https://neat-python.readthedocs.io/en/latest/#) for environment exploration and collision avoidance.

[NEAT-python](https://neat-python.readthedocs.io/en/latest/#) is an evolutionary algorithm for creating artificial neural networks. Using this we create an **Ant Agent** which is trained to navigate its environment while avoiding obstacles, staying within the boundaries and succefully reaching the goal/flag.

## Agent Configuration
In this implementation, the Ant is allowed to perform 3 actions; move forward, rotate right and rotate left. The agent has a 45 degree view on either side from its center, upto a distance of 60 pixels as indicated by the yellow lines. The angle and distance of view may be varied. The Ant is able to detect the red bounding boxes of objects and the wall or the window edges. The Ant does not detect other Ants as obstacles.

3 inputs are passed to the neural network of the agent: (Obstacle distance, Angle subtended by obstacle, Angle subtended by Goal/Flag). In this implemenatation, we have used a tanh activation function by default but you may use any other activation function. We start with a population of 50 Ants which are initialized by NEAT with random weights and biases. You may refer to the config file and [NEAT-python documentation](https://neat-python.readthedocs.io/en/latest/#) for further details.

## Reinforcement Learning

To train the Ants, the following reward system is used:
* +0.1 - any action
* +0.5 - moving towards the goal
* +100 - reaching the goal
* -100 - staying the in the same coordinates for more than 30 time steps
* -100 - any collision
* -0.1 - moving away from the goal

If any collision occurs, the particular ant is killed and removed from that iteration.
The above values may be experimented with.

### Maps

This map generates a random set of obstacles that the ants must navigate across and reach the goal successfully. To speed up the learning process, Map 2 given below is used to train on first to get the ant to better learn to navigate around walls and obstacles. When the Ants are then put into Map 1 which is a more dynamic environment, with randomly placed obstacles, they are able to navigate to the goal much faster. 
The 'first sucess' checkpoint is saved after training on Map 2 and then used in Map 1.

###### Map 1
<img src="map1.gif" height="50%" width="50%"> <img src="map2.gif" title="Map2" height="50%" width="50%">
