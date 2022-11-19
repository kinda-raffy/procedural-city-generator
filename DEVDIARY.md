# Development Diary
This is a *template* for your dev diary in PS2.
Feel free to edit as you see fit e.g., based on your progress updates, hurdles encountered and circumnvented.
Make sure to log one comprehensive update per student, per each week of our teaching term.
Please, get in touch with teaching staff for any questions around this or otherwise post on Microsoft Teams.

# Mandatory Student's contributions
Please, specify your individual contributions to the project **as a percentage**.
Default is a *25% contribution for each student*. However, please modify as necessary, if that is not the case.

‼ Everyone contributed equally even though on github insights it might look quite skewed. This is due to (in the case of Raf and Matt) pair programming on the same local machine. Most of Matt's work was pushed under my name.

# Development Diary Activities
Please, report your key activities in each week this assignment is running.  

**Week 1**
* Student 1 [Adrian] S3889401
    * Read chapter 1 & 2 on textbook
    * Setup VS Code, and Minecraft on Windows
    * Implemented Hello Minecraft, and experimented further with the API
    * Implemented prototype fpr height mapping, grid generation, tile class for project.
    * Pair programmed with Harry to further develop the village planner class. This class is responsible for the initial planning of the village, and highly respects terrain:
        * Added Graph system that maps connected tiles based on constraints such as tile type and height difference.
        * Harry's Breadth first search determines which "island" of connected tiles is largest.
        * We implemented a simple check to find a center point of this "island", which is crucial for path connection.
        * We also began building the system which will designate valid house tiles to be passed to the house class.
    * Figured out how to use the preview tab on Github to avoid pushing to the repo too many times (sorry guys)
* Student 2 [Harry]
    * Read chapter 1 & 2 on textbook
    * Setup VS Code, and Minecraft on Windows 11
    * Implemented Hello Minecraft!
    * Generated staircase as per workshop class, and did some small self-guided exercises with the API.
    * Worked with Adrian in alternating pair programming roles to develop the prototype basis of our town layout system. This system includes:
         * A designed hierarchy of interellated classes with their respective methods: Village, Grid and Tile.
         * Adrian's initial work creates a grid of evenly spaced tiles, maps each tile to its respective terrain and finds the ground height of that tile.
         * Code we implemented together generates a graph on these tiles, generating edges only when the world terrain can be respected.
         * I implemented a specialised breadth first search algorithm in the Grid class to find the largest connected area of the graph - the ideal village location.
         * Once the largest connected area was defined, Adrian and I worked together again to develop an algorithm that finds the center tile of this area.
   * Future forecast: Redevelop the grid generation system to dynamically build out a grid based on the terrrain, and up to a maximum number of tiles, using the already existing grid system as a backup in case the terrain is not suitable enough. This saves on wasted space in the village generation and limits terraforming if at all possible.
* Student 3 [Matt]
    * Read chapter 1 & 2 on textbook
    * Setup PyCharm, and Minecraft on Windows
    * Implemented Hello Minecraft!
    * Followed the Raspberry Pi tutorial for the API
    * Planned out the house Generator class with Raf and decided where the generation of the housed would begin and function
    * started construction the room functions
* Student 4 [Rafat] s3897093
    * Activities:
      * Read chapter 1 & 2 on textbook
      * Completed set up Minecraft Java Edition
      * Learned how to configure mc spigot
      * Implemented Hello Minecraft!
      * Completed stairs assignment
    * Project:
      * Generated the design of individual rooms in python
      * Created a house and room class:
           * Created a general road map for both house and room classes with Matt
           * Designed the house class for future randomisation implementation
           * Redone the positioning of the room class to work alongside adrians code.
           * Included two different roof designs: base and angled-flat.
           * Created a versatile door function that simplifies the annoying door placement in mc.
           * Created two different door designs
    * Others:
      * Transferred all code from private github repo to github classroom

**Week 2**

* Student 4 [Rafat] s3897093
   * Activities:
     * Installed and ran Kali Linux on a virtual machine
     * Completed all terminal activities
     * Did a threat analysis on RMIT
   * Project:
     * My commit messages from 12th - 18th best highlight my activity. I have structured my contributions via revisions. 
       My revisions have their own roadmaps, but for reference revision 3 aims to fully meet the marking criteria. I have added additional details to my messages for the sake of clarity:
       - Revision 1:
            * Fixed python env and directory for our project
            * Merged all house code into house.py
            * Programmed first working revison of random generator with Matt.
            * Fixed a check neighbours inside main generator for loop.
            - Pyramid level foundation always ensures access to doorway
            - Created a main block dictionary
            - Created a sand biome dictionary for sand biomes
            - Modulized the house code into smaller functions, more manageable functions.
            - Fully implemented random biome generation with the current code.
            * Added random internal wall generation
            * Added main doors
            * House.py now can randomly generate a basic single story house with multiple rooms.
            doors to each rooms are yet to be added
      - Revision 2:
        - Fully revised random generator to become far more efficent.
          The new version is more simpler, uses less memory and may be easily implemented for double story generation.
        - House class can now generate double story rooms with each room being 5 by 5. No internal doorways or stairs
          has been implemented at this stage.
        - House pillar placement code has been attampted and works partly. Due to high complexity and low outcome, this may be abandoned later.
        - Introduced sleep statements to assist in memory management // Something to look into
        - Bug fixes in create_level. The generator has more broader checks to prevent unwanted rooms from passing through.
        - Reworked the way we manage. They now have a set structure making them more predictable to index.
        - Seperated foundations for both upstairs and downstairs.
        - Half way there with the stair rooms.
        - Building aesthetic changes to be more consistent.
        - Introduced castle shaped roofs.
* Student 3 [Matt]
   * Activities:
      - Competed all activities including downloading and running kali linux on my laptop.
   * Project:
      - Pair programmed with raf to create the level generator. 
      - Wrote and debugged conditionals for the generator so that room generation makes sense (rooms will not generate in ways that does not make any sense)
      - Stitched together the two classes for functions to rrun smoothly
      - Created the generated rooms list in which most of our code relies upon.
* Student 2 [Harry]
   * Activities:
      * Conducted a threat assessment for Bloomberg L.P.
      * Followed along throughout the workshop to set up a Kali Linux Environment on a Virtual Machine.
   * Project:
      * Adrian and I pair-programmed throughout the week to develop and complete a number of algorithms acting on our grid data structure, as well as our village class.
         * Breadth first search to find the largest connected area of our matrix allowed us to begin generating a connected grid organically, through another modified breadth first search algorithm that I completed the first iteration of independently, then reiterated and debugged as a pair with Adrian.
         * Began to build out the Village class by designing the town_planner method, which allocates house plots and road tiles, then instantiates houses and passes the necessary information to the house class, being developed by Raf and Matt.
         * Implemented roads by designing a system around Dijkstra's shortest path algorithm, running on our grid data structure. Whilst we'd initially tried to implement A* to determine these roads, we never quite got this implementation working and decided to stick to the more stable Dijkstra's pipeline.
         * Implemented a system that works alongside Dijkstra's algorithm to determine the door placement on houses, according to the candidate tile that is most easily reached.
         * Implemented a small system that allows for the village to determine its biome using an enumeration. Broadly tried to refactor our existing code to eliminate as many unneccessary string comparisons as possible, since Adrian read they might be slowing down an already very slow system.

* Student 1 [Adrian] S3889401
   * Activities:
      * Conducted threat assessment for Bunnings Warehouse franchise (Workshop 1)
      * Workshop 2: Created VM of Linux Environment.
   * Project:
      * Continued development of Village planner with Harry (Pair Programming)
         * Almost complete redesign of grid generation: simple matrix to Breadth first search. Harry developed this code independantly and it was almost at a working state. Together we fixed this algorithm.
         * Developed House plot designator. Builds House objects with their required starting information.
         * Changed file structure. Village.py now contains all initial generation code. VillagePlanner is obsolete.
         * Began development of new height finding algorithm to replace MCPI's get_height function. MCPI's implementation is slow, and is the bottleneck for village generation. This was abandoned due to poor performance, presumably due to server's performance limitations.
         * Attempted to implement A* algorithm for path finding, instead used Djikstra's alogorithm to plot mock roads.
         * Implemented Biome selector for houses, with scope for water houses (not yet implemented in house class)
         * Integrated village generator with house generator with correct door information.
         * Implemented road builder, which takes results from path finding algorithm and aesthetically connects them.


**Week 3**

* Student 4 [Rafat] s3897093
   - Activities:
     - Used PC Part Picker to find ram given a budget as part of an excercise.
     - Completed reading materials surrounding RAM and CPU architecture.
   - Project:
    
     - Revision 3:
      - Integrated house.py with village.py
      - Brought everything under the same directory
      - Seperated matpack dictionary to a different file
      - Cleaned up and further optimized the performance of house.py.
      - Added in sleep timers after significant setBlocks to prevent drain data error.
      - Revised our level generation code to be more thorough. Now accepts rooms types.
      - Added pools, pool sizes, pool wall types and pool shades. All randomised
      - Added in windows. All randomised.
      - Improved upon room placement code.
      - Added different sorts of barriers for pools
      - Indoor and outdoor pools added.
      - Added in stairs and stair room placement.
      - Added in more entries into sand and grass biomes dictionary.
      - House.py now supports different biome types
      - Made the code much more modular into seperate functions (especially for the room placement)
      - Readied the code for furnishing functions
    
    - Revision 4:
        - Implemented a random furniture generator to furnish rooms in accordance to their respective sizes.
        - Added in 2 more roof types
        - Compartmentalised the house function into much smaller functions. This readies the code for apartment level generations.
        - Sub-Revision 4.5:
            - Fully fixed random furniture generation
            - Added a centralised dictionary file for easy edit
            - Added 1 more internal wall type
            - Cleaned up all code to meet PEP 8 standards
            - Added additional mat packs for greater customisable
            - Experimented with mod spawns
            - Greatly expanded upon the blocks dictionary. (now also contains positions of certain blocks)
        - Sub-Revision 4.6:
            - Added in 5 more desert configurations
        - Sub-Revision 4.7 - 4.12:
            - Added in 12 more water configurations
            - Fixed a pool fence issue
            - Fixed grass biome dictionary to accept more matpack options
            - Added 5 more configs to grasslands
            - Changed mc.posttochats to print statements
            - Added 3 more configs to furnishing
      
    - Revision 5:
        - Added 27 more entries to furniture dictionary
        - Disasters now have a 1 in 196 chance of spawning with each room spawn (lab explosion and kitchen fires)
        - Standardised everything to pep8
        - Uncommented foundations
        - Fixed certain typos
        - Added more entries to blocks dict
        - Added in an additional roof type
      
    - Revision 6:
        - Modified the house function to now support triple story houses. (4/10 chance of spawning when a double story has been created)
        - General code practice improvements
        - Added in a long staired roofs
        - Experimented with shaded roofs but decided against it due to adoption complexity with our current code structure.
   
    - Revision 7:
        - Adds support for multi-level apartment complexes with a max height 40 blocks
        - Due to stricter maintenance requirements, apartments have an 1/2744 chance of spawning a disaster per room spawned.
        - Restructured our init call with a simple bob_the_bulider function. Bob acts as a traffic warden between 2 major core functions: house and apartment.
          Bob will build it depending on biome info.
        - Added in new global values to support apartments.
        - Got rid of magic numbers in our code.
        - Added an apartment mat-pack with 5 different configs.
    - Revision 8:
        - Added support for a chance to randomly generate 60 - 80 block skyscrapers 
          in the apartment biome (within grasslands).
        - Added in 5 more apartment matpacks.
        - Skyscrapers randomly follows a different architectural rulebook (for example: some may have a fat base and skinny top 
          while others may have a skinny base and fat top).
    - Presentation:
        - Wrote a script for our video presentation and narrated a part of the video.
    - Closing thoughts:
        - I like
    
   - Others:
       - Added instructions on top of house.py
       - Added an image of shrek for good luck in our image folder.   
* Student 3 [Matt]
   * Activities:
      - Read up on materials on CPU and RAM architecture. 
   * Project:
      - Created pools to add to our houses
      - Added in fences to our pools
      - Wrote conditionals for our remove walls function to create bigger rooms
      - Created different types of windows which will be than randomised on room walls.
      - Wrote the add windows function so that the generator may make logical decisions on where to pace windows
      - Created the stair room type and made different types of stairs which are randomly genrated.
      - Implemented the place_furniture and add furniture functions which places furniture on various zones, scaling it up to room length.
   * Others: 
* Student 2 [Harry]
   * Activities:
      * Basically just browsed RAM online for a bit and looked up what abbreviations like DIMM stood for. Began to appreciate how the different elements of memory correspond to performance.
      * Learned about RAM and CPU architecture generally through readings.  
   * Project:
      * Adrian and I had largely completed our share of the project by this time, and split up to complete smaller, self-contained tasks.
      * I designed a number of town centers to be randomly selected according to the biome of each village, as well as the system to facilitate this randomisation.
      * Went through and refactored some code to remove extraneous lines and magic numbers, as well as to make the parameters of village generation more clear.
      * Acted in a largely advisory capacity to help Adrian complete the implementation of randomised streetlights.
      * Added a small number of docstrings to elucidate the function of our classes, as well as the unweildy town_planner method.
      * Tested a number of village sizes with Adrian to ensure our miscellaneous items were working together and our code was modular and scalable enough to support villages of massively exaggerated sizes (see video recording). 
* Student 1 [Adrian] S3889401
   * Activities: 
       * Investigated RAM and CPU purchasing at given budgets
       * Read and explored about RAM and CPU architecture
   * Project:
       * Implemented fancier Roads
       * Implemented Street lamps and a corresponding algorithm for their generation
       * Implemented Street vendor huts that have random pallets, centered around TC
       * Adjusted Village size parameters
       * Planning/Roads/Misc part of assignment completed by Thursday 7pm
       * Filmed 5min recap for project
       * enabled water biomes for new water house configurations
   * Others: 
