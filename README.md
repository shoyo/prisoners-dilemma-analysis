 # Iterated Prisoner's Dilemma Analysis Tool
 
 ## About
The "prisoner's dilemma" is a scenario in game theory where two participants must independently choose to either cooperate for a mutual gain or betray the other for a greater personal gain. If both participants choose to betray one another, the total gain for both participants is lower than if both participants had just cooperated. This README assumes a basic understanding of this scenario and its reward schemes. To learn more, you can visit the [Wikipedia page](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma).

In the _iterated_ prisoner's dilemma, two players continuously play out the scenario for a given number of rounds and aim to maximize their total gain. The way a player behaves each round is determined by its _strategy_. Should a player aim to be as cooperative as possible? Or maybe seek to exploit their partner? Maybe a mix of both?

The motivation behind this project is to create a tool that can answer these questions through data visualization.

An initial "population", consisting of players each with its own strategy, plays the iterated prisoner's dilemma game. In each _generation_, each player plays against every other player in the population. Successive generations are created based on how effective each strategy was at producing gain. Strategies that were more effective in a given generation are more likely to produce offspring in the next generation to carry on their strategy. The population distribution over the course of each generation is then graphed.
  
tl;dr Strategies compete. Better strategies reproduce more successfully. Repeat. Graph.


## Getting Started
### Prerequisites
  * [Python 3](https://www.python.org/) (version 3.6.3 or later)
  * [Matplotlib](https://matplotlib.org/) (version 2.2.0 or later)
  * [NumPy](http://www.numpy.org/) (version 1.14.1 or later)
  
### Installation
Python 3 can be installed via the official Python page (https://www.python.org/).
When Python 3 is installed, the pip3 package manager will also be installed by default.

To install Matplotlib, type into the command line:

    pip3 install matplotlib
    
To install NumPy, type into the command line:

    pip3 install numpy

### Running the Simulation Tool
After obtaining a local copy of this repository, navigate to the `IPDsrc` directory.  
To run the GUI and start using the application, type into the command line:

    python3 gui.py
 
## Brief Overview of Some Strategies
Strategies are a predetermined set of rules to play to iterated Prisoner's Dilemma game. Some of the strategies implemented in this project are listed below.
  * Kantian: 
  
     Always cooperates
     
  * Defector:
  
     Always betrays
     
  * Tit-for-Tat:
  
     Aims to cooperate. If the opponent betrayed in the last round, then betrays.
     
  * Tit-for-2-Tats:
  
     Aims to cooperate. If the opponent betrayed in the last two rounds, then betrays.
  
  * Tester: 
  
     The "Tit-for-2-Tats" exploiter. It acts cooperatively at first, but "tests" randomly by betraying and following up with a turn of cooperation. If the opponent doesn't retaliate, then it switches off between cooperating and betraying for the rest of the game.
  
  * ...and many more!

## Samples
The GUI of the IPD analysis tool. The initial population and simulation settings can be set on the left, and the corresponding graph will be drawn on the right. 
![alt text](https://github.com/shoyo-inokuchi/iterated-prisoners-dilemma/blob/master/samples/default.png)

Every currently-implemented strategy within this project:
![alt text](https://github.com/shoyo-inokuchi/iterated-prisoners-dilemma/blob/master/samples/all.png)

Tit-for-Tat acts as an effective strategy against an uncooperative strategy like Defector:
![alt text](https://github.com/shoyo-inokuchi/iterated-prisoners-dilemma/blob/master/samples/tft_vs_defectors.png)

A forgiving strategy like Tit-for-2-Tats can be effective among strategies that are not overly exploitative:
![alt text](https://github.com/shoyo-inokuchi/iterated-prisoners-dilemma/blob/master/samples/tfts.png)

Introducing Tester, a "Tit-for-2-Tats exploiter", to the population shown above quickly changes things:
![alt text](https://github.com/shoyo-inokuchi/iterated-prisoners-dilemma/blob/master/samples/tfts_tester.png)

*Simulations with identical settings may produce varied results (especially with smaller population sizes or rounds) due to the probabilistic nature of the breeding mechanism. More details concerning implementation can be read on [evolution-ipd.pdf](./evolution-ipd.pdf).*


## Contributions
Testing, bug hunting, implementing more strategies etc. are all welcome!  
You can contribute by submitting an issue or pull request.

## License
The code within this repository is MIT licensed. See [LICENSE.md](./LICENSE.md) for details.
