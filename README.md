# Autonomous Self-Parking System (AI Smart Parking)

An interactive AI simulation built with **Python** and **Pygame** that demonstrates how an autonomous vehicle can scan its environment, detect obstacles, and find the optimal path to a parking spot using the **A* Search Algorithm**.

## 🚀 Features
- **Environment Scanning:** Real-time laser scanning simulation to detect free vs. occupied areas.
- **Pathfinding AI:** Uses the **A* (A-Star) Algorithm** to calculate the shortest and safest path to the target.
- **Dynamic Obstacles:** Randomly generated pillars and other cars to test the AI's efficiency.
- **Visual Dashboard:** Real-time statistics showing the number of cars, occupied space, and free space.
- **Interactive UI:** Smooth animations and clear "Success" notifications upon parking.


<img width="1366" height="768" alt="ai1 jpg" src="https://github.com/user-attachments/assets/98778b87-742c-40ea-b7cc-19c04684d358" />
<img width="1366" height="768" alt="ai2 jpg" src="https://github.com/user-attachments/assets/b0dd013b-7d95-4885-b5ce-41c666ad6e19" />
<img width="1366" height="768" alt="ai3 jpg" src="https://github.com/user-attachments/assets/5cbf4a8f-b77f-4fec-afda-f8fc8611df8f" />
<img width="1366" height="768" alt="ai4 jpg" src="https://github.com/user-attachments/assets/9936a9d7-ec8a-4f07-9bf1-330e64ef2382" />
<img width="1366" height="768" alt="ai5 jpg" src="https://github.com/user-attachments/assets/95d84f67-4915-4281-8aeb-e8cedd51c099" />
<img width="1366" height="768" alt="ai6 jpg" src="https://github.com/user-attachments/assets/ed8cd04f-b2f8-4cf3-b1ab-5aa0dc437383" />

<img width="1366" height="768" alt="finalresult" src="https://github.com/user-attachments/assets/f53d22fc-fb37-4726-9ad5-c1f80c93249d" />

## 🛠️ Technologies Used
- **Language:** Python 3.x
- **Libraries:** - `Pygame`: For the graphical interface and animations.
  - `PriorityQueue`: To optimize the A* algorithm performance.
  - `Math & Random`: For environmental generation and physics.

## 🧠 How the AI Works
1. **Perception:** The car starts by scanning the area (360 degrees) to map out obstacles.
2. **Decision Making:** The A* algorithm evaluates the grid, considering the distance to the target (Heuristic) and the cost of movement.
3. **Execution:** The car follows the generated path points with smooth movement interpolation until it reaches the `COLOR_TARGET` spot.

## 🎮 How to Run
1. Make sure you have Python installed.
2. Install Pygame:
   ```bash
   pip install pygame
