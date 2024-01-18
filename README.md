# putz-agent
These are some changes
## State Machine
Resets every week to keep it simple. Can be extended of course in the future. Can also do two operational modes. Simple mode where agent just tells user what to clean and schedules them for a standard day (Sunday?). If user wants to schedule different day, they can reschedule i guess. 

1. Send Users notification to schedule cleaning this week (Randomise cleaning areas or do cleaning rotation ?)
2. User sends prefered day to clean
3. Agent reminds user to clean maybe the day before / on the day ?
4. Agent reminds user if they forgot until they do it! (Could become progressively worse by insulting the user and spamming them if they do not get it done xD)
5. User sends confirmation that they cleaned
6. Agent notes this down (optional)

![State Diagram of agent](/project_documentation/putz_agent_state_diagram.drawio.png?raw=true "State Diagram")

## Penalty Cleaning
If someone misses their cleaning task, they will receive a punishment point. These will be saved in a file. The agent then decides the assignemnt of the cleaning areas of the next week with these points in mind. This will be done in a simple manner. There are three cleaning areas. For each cleaning area, the agent will pick a random element from an array (that contains the names of all wg members). If the user a has n punishment points, then n additional a elements will be added to the array. Therefore the chance for a user to have to clean multiple areas increases depending on how many points you have. This also has the effect that in some weeks, other wg members might not have to clean at all.
