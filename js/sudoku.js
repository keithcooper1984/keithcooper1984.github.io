var lst = new Int8Array([1,2,3,4,5,6,7,8,9]);
var sqrt = Math.sqrt(lst.length);
var grid = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]];

function shuffle(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

shuffle(lst)

function print_square(square) {
    for(var i = 0; i < square.length; i++) {
      console.log(square[i]);
    }
}

function square(arr, sqrt) {
    shuffle(arr);
    var start = 0;
    var square = [];
    while (start < arr.length) {
        var temp = arr.slice(start, start + sqrt);
        square.push(temp)
        start += sqrt;
    }
    return square;
}

var sq = square(lst,sqrt);

function initialise(arr, sqrt, grid) {
    var start = 0;
    while (start < arr.length){
        var sq = square(arr, sqrt);
        for (var i = 0; i <sqrt; i++){
            for (var j = 0; j < sqrt; j++) {
                grid[i + start][j + start] = sq[i][j];
            }
        }
        start += sqrt;
    }
}

initialise(lst, sqrt, grid);


function check_row(arr) {
    arr = arr.sort();
    for (var i = 1; i < arr.length; i++) {
        if (!(arr[i] > 0 && arr[i] <= 9)){
            return false;
        }
        else if (arr[i] == 0){
            continue;
        } else if (arr[i] == arr[i - 1]){
            return false;
        }
    }
    return true;
}


function check_square(arr2d) {
    var flattened = arr2d.flat();
    return check_row(flattened);
}

var example_arr2D = [
    [1,3,12],
    [4,15,6],
    [7,8,2]];


function full_check(arr2d) {
    
    // check rows
    for (var i = 0; i < arr2d.length; i++){
        var status = check_row(arr2d[i]);
        if (status == false) {
            return false;
        }
    }
    
    //check cols
    for (var j = 0; j < arr2d.length; j++){
        const arrayColumn = (arr, n) => arr.map(x => x[n]);
        var col = arrayColumn(arr2d, j);
        var status = check_row(col);
        if (status == false) {
            return false;
        }
    }
    
    //check squares
    // TODO refactor
    for (var z = 0; z < arr2d.length; z += 3){
         var square_arr1 = [bad_grid[z][0],bad_grid[z][1],bad_grid[z][2],bad_grid[z+1][0],bad_grid[z+1][1],bad_grid[z+1][2],bad_grid[z+2][0],bad_grid[z+2][1],bad_grid[z+2][2]];
         var square_arr2 = [bad_grid[z][3],bad_grid[z][4],bad_grid[z][5],bad_grid[z+1][3],bad_grid[z+1][4],bad_grid[z+1][5],bad_grid[z+2][3],bad_grid[z+2][4],bad_grid[z+2][5]];
         var square_arr3 = [bad_grid[z][6],bad_grid[z][7],bad_grid[z][8],bad_grid[z+1][6],bad_grid[z+1][7],bad_grid[z+1][8],bad_grid[z+2][6],bad_grid[z+2][7],bad_grid[z+2][8]];
         var status = check_row(square_arr1) && check_row(square_arr2) && check_row(square_arr2);
         if (status == false) {
            return false;
        }
    }
    return true;
}

function next_empty (arr2d){
    for (var i = 0; i < arr2d.length; i++){
        for (var j = 0; j < arr2d.length; j++){
            if (arr2d[i][j] == 0) {
                console.log(i,j);
                return [i,j];
            }
        }
    }
    return [-1,-1];
}

function solve (arr2d){
    var row, col  = next_empty(arr2d);
    
    if (row = -1) {
        return arr2d;
    }

    for(let i = 1; i <= 9; i ++){
        if (full_check(arr2d)){
            arr2d[row][col] = i;
            solve(arr2d);
        }
    }

    if (next_empty(arr2d)[0] !== -1){
        arr2d[row][col] = 0;
    }
}
