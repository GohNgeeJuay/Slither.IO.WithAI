from pygame.math import Vector2
#Possible state space includes:
#Snake's entire body
#Snake's direction
#Enemy snake's entire body
#Enemy snake's direction
#Snake's apple
#Enemy snake's apple
#Maybe use rgb of screen surface Ref: https://www.pygame.org/docs/ref/surfarray.html#pygame.surfarray.array2d

#Action space:
#Up, down, left, right (depending on the snake's current direction)

#Neural network:
#Input layer = 
#Output layer = 4 nodes
#Hidden layer = 

#Reward:
#+10 for eating fruit
#-10 for dying
#+0.05 for surviving

class Agent:

    def __init__(self, args, env):
        pass
        # set hyperparameters
        # self.max_episodes = int(args.max_episodes)
        # self.max_actions = int(args.max_actions)
        # self.discount = float(args.discount)
        # self.exploration_rate = float(args.exploration_rate)
        # self.exploration_decay = 1.0/float(args.max_episodes)
    
        # # nn_model parameters
        # self.inputDim = 
        # self.out_units = env.action_space.n
        # self.hidden_units = int(args.hidden_units)
        
        # # construct nn model
        # self._nn_model()
    
        # # save nn model
        # self.saver = tf.train.Saver()

    def getAction(self):
        pass
