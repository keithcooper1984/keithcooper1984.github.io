// Load boards from file or manually
const easy = [
    "6------7------5-2------1---362----81--96-----71--9-4-5-2---651---78----345-------",
    "685329174971485326234761859362574981549618732718293465823946517197852643456137298"
  ];
  const medium = [
    "--9-------4----6-758-31----15--4-36-------4-8----9-------75----3-------1--2--3--",
    "619472583243985617587316924158247369926531478734698152891754236365829741472163895"
  ];
  const hard = [
    "-1-5-------97-42----5----7-5---3---7-6--2-41---8--5---1-4------2-3-----9-7----8--",
    "712583694639714258845269173521436987367928415498175326184697532253841769976352841"
  ];

  // Create Variables
  var timer;
  var timeRemaining;
  var lives;
  var selectedNum;
  var selectedTile;
  var disableSelect;

  window.onload = function () {
      //Run startgame function when button is clicked
      id("start-btn").addEventListener("click", startGame);
      //add event listener to each number in number container
      for(let i = 0; i < id("number-container").children.length; i++) {
          id("number-container").children[i].addEventListener("click", function() {
            //if selecting is not disabled
            if (!disableSelect) {
                //if number is already selected
                if (this.classList.contains("selected")) {
                    this.classList.remove("selected");
                    selectedNum - null;
                }
                else {
                    //deselect all other numbers
                    for(let i = 0; i < id("number-container").children.length; i++) {
                        id("number-container").children[i].classList.remove("selected");
                    }
                    //select it and update selectedNum var
                    this.classList.add("selected");
                    selectedNum = this;
                    updateMove();
                }
            }
          });
      }
  }

  function startGame() {
      //Choose board difficulty
      let board;
      if (id("diff-1").checked) board = easy[0];
      else if (id("diff-2").checked) board = medium[0];
      else board = hard[0];

      //Set Lives to 3 and enable selecting numbers and tiles
      lives = 3;
      disableSelect = false;
      id("lives").textContent = "Lives Remaining: 3";
      // Creates board based on difficulty
      generateBoard(board);
      //Starts the timer
      startTimer();
      //sets theme based on input
      if (id("theme-1").checked){
          qs("body").classList.remove("dark");
      }
      else {
        qs("body").classList.add("dark");
      }
      //show number container
      id("number-container").classList.remove("hidden");
  }

  function startTimer() {
      //set time based on input
      if (id("time-1").checked) timeRemaining = 180;
      else if (id("time-2").checked) timeRemaining = 300;
      else timeRemaining = 600;
      //sets timer for first second
      id("timer").textContent = timeConversion(timeRemaining)
      //sets timer to update every second
      timer = setInterval(function() {
        timeRemaining--;
        if (timeRemaining === 0) endGame();
        id("timer").textContent = timeConversion(timeRemaining);
      }, 1000)
  }

  //convers seconds into MM:SS string
  function timeConversion(time) {
    let minutes = Math.floor(time / 60);
    if (minutes < 10) minutes = "0" + minutes;
    let seconds = time % 60;
    if (seconds < 10) seconds = "0" + seconds;
    return minutes + ":" + seconds;
  }

  function generateBoard(board) {
      //Clear previous board
      clearPrevious();
      //Let used to increment tile ids
      let idCount = 0;
      //Create 81 tiles
      for (let i = 0; i < 81; i++) {
          let tile = document.createElement("p");
          if (board.charAt(i) != "-") {
             //set tile text to correct number
             tile.textContent = board.charAt(i);
          }
          else {
              //add click event listener to tile
              tile.addEventListener("click", function() {
                if (!disableSelect) {
                    if (tile.classList.contains("selected")){
                        tile.classList.remove("selected");
                        selectedTile = null;
                    }
                    else {
                        for (let i = 0;i < 81; i++) {
                            qsa(".tile")[i].classList.remove("selected");
                        }
                        // add selection and update variable
                        tile.classList.add("selected");
                        selectedTile = tile;
                        updateMove();
                    }
                }
              });
          }
          //assign tile id
          tile.id = idCount;
          //increment for next tile
          idCount++;
          //Add tile class to all tiles
          tile.classList.add("tile")
          if ((tile.id > 17 && tile.id < 27) || (tile.id > 44 && tile.id < 54)) {
              tile.classList.add("bottomBorder");
          } 
          if ((tile.id + 1) % 9 == 3 || (tile.id + 1) % 9 == 6 ){
              tile.classList.add("rightBorder");
          }
          //Add tile to board
          id("board").appendChild(tile);
      }
  }

  function updateMove() {
      //if a tile and number is selected
      if (selectedTile && selectedNum) {
          //set tile to correct number
          selectedTile.textContent = selectedNum.textContent;
          // if number matches corresponding number in solution key
          if (checkCorrect(selectedTile)){
            //deselects the tile
            selectedTile.classList.remove("selected");
            selectedNum.classList.remove("selected");
            //clear variables
            selectedNum = null;
            selectedTile = null;
            // check if board is completed
            if (checkDone()) {
                endGame();
            }
            // If number does not match solution key
          }
          else {
              //disable selecting new numbers for one second
              disableSelect = true;
              // turn number red
              selectedTile.classList.add("incorrect")
              setTimeout(function () {
                //Subtract lives by 1
                lives--;
                //if no lives left end game
                if (lives === 0) {
                    endGame();
                }
                else {
                    //if lives !== 0, update text on screen
                    id("lives").textContent = "Lives Remaining: " + lives;
                    disableSelect = false;
                }
                selectedTile.classList.remove("incorrect");
                selectedTile.classList.remove("selected");
                selectedNum.classList.remove("selected");
                selectedTile.textContent = "";
                selectedTile = null;
                selectedNum = null;
              }, 1000);
          }
      }
  }

  function checkDone() {
      let tiles = qsa(".tile");
      for (let i = 0; i < tiles.length; i++) {
          if (tiles[i].textContent === "") return false;
      }
      return true;
  }

  function endGame() {
      //disable moves and stop timer
      disableSelect = true;
      clearTimeout(timer);
      //display win or lose message
      if (lives === 0 || timeRemaining == 0) {
          id("lives").textContent = "You Lost!";
      } else {
        id("lives").textContent = "You Won!";
      }
  }

  function checkCorrect(tile){
      //Set solution based on difficulty selection
      let solution;
      if (id("diff-1").checked) solution = easy[1];
      else if (id("diff-2").checked) solution = medium[1];
      else solution = hard[1];

      // if tiles number == solution number
      if (solution.charAt(tile.id) == tile.textContent) return true;
      else return false;
  }

  function clearPrevious() {
      let tiles = qsa(".tile");
      //Remove each tile
      for (let i = 0; i < tiles.length; i++) {
          tiles[i].remove();
      }
      //If there is a timer clear it
      if (timer) clearTimeout(timer);
      //Deselect Numbers
      for (let i = 0; i< id("number-container").children.length; i++) {
           id("number-container").children[i].classList.remove("selected");
      }
      //Clear selected Variables
      selectedTile = null;
      selectedNum = null;
  }

  function qs(selector) {
      return document.querySelector(selector);
  }

  function qsa(selector) {
      return document.querySelectorAll(selector)
  }

  function id(id) {
      return document.getElementById(id);
  }