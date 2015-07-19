// converts a canvas coordinate to a board coordinate
function convertToGridCoord(input){
	input = snapToGridCorner(input)
	input -= MIN;
	input /= STEP;
	return input;
}

// snaps a canvas coordinate to the top-left corner of the enclosing board square 
function snapToGridCorner(input){
	input -= MIN;
	input -= (input % STEP);
	input += MIN;
	return input;
}

// converts a board coordinate to the canvas coordinate of the top-left corner of the board square
function convertToCanvasCoord(input){
	input *= STEP;
	input += MIN;
	return input;
}

// draw text at a given location
function drawText(text, x, y, fontSpec){
	if(fontSpec === undefined){
		fontSpec = "20px sans-serif";
	}
	ctx.font = fontSpec;
	ctx.fillStyle = "#000000";
	ctx.fillText(text, x, y);
}

// draw a line between two points
function drawLine(startX, startY, endX, endY){
	ctx.beginPath();
	ctx.moveTo(startX, startY);
	ctx.lineTo(endX, endY);
	ctx.stroke();
}

// draw and fill an arbitrary polygon
function drawPolygon(coordinates){
	ctx.beginPath();
	ctx.moveTo(coordinates[0][0], coordinates[0][1]);
	for(var i = 1; i < coordinates.length; i++){
		ctx.lineTo(coordinates[i][0], coordinates[i][1]);
	}
	ctx.lineTo(coordinates[0][0], coordinates[0][1]);
	ctx.stroke();
	ctx.fill();
}

// draw a circle; x and y must be canvas coordinates of the top-left of the grid square
// offest and size have default values which preserve the above behavior
// to have the circle drawn around the passed point, set offset = 0
function drawCircle(x, y, size, offset, fill){
	if(size === undefined){
		size = 3/8;
	}
	if(offset === undefined){
		offset = STEP / 2;
	}
	if(fill === undefined){
		fill = true;
	}
	ctx.beginPath();
	ctx.arc(x+offset, y+offset, STEP*size, 0, Math.PI*2);
	if(fill){
		ctx.fill();
	}
	ctx.stroke();
}

// fill a board space with the given color
function drawSpace(boardX, boardY, color){
	var x = convertToCanvasCoord(boardX);
	var y = convertToCanvasCoord(boardY);
	ctx.fillStyle = color;
	ctx.fillRect(x+1, y+1, STEP-2, STEP-2);
}

// draw a piece in a space
function drawPiece(boardX, boardY, piece){
	// convert board coords to canvas coords
	var x = convertToCanvasCoord(boardX);
	var y = convertToCanvasCoord(boardY);
	// set the appropriate color
	switch(piece.color){
		case PieceColors.EMPTY: //if the space is empty, there's no piece to draw
			return;
			break;
		case PieceColors.WHITE:
			ctx.strokeStyle = "#000000";
			ctx.fillStyle = "#ffffff";
			break;
		case PieceColors.BLACK:
			ctx.strokeStyle = "#000000";
			ctx.fillStyle = "#000000";
			break;
	}
	// draw the piece
	switch(piece.type){
		case PieceTypes.EMPTY:
			break;
		case PieceTypes.WARPLING:
			drawCircle(x, y);
			break;
		case PieceTypes.KING:
			drawPolygon([[x + STEP / 8, y + STEP / 8],[x + STEP / 2, y + STEP /2], [x + 7 * STEP / 8, y + STEP / 8], [x + 7 * STEP / 8, y + 7 * STEP / 8], [x + STEP / 8, y + 7 * STEP / 8]]);
			drawCircle(x, y, 3 / 16, STEP / 2, false);
			break;
		case PieceTypes.KNIGHT:
			drawPolygon([[x + STEP / 8, y + 7 * STEP / 8], [x + STEP / 4, y + STEP / 8], [x + 3 * STEP / 8, y + STEP / 8], [x + 7 * STEP / 8, y + STEP / 4], [x + 7 * STEP / 8, y + 3 * STEP / 8], [x + STEP / 2, y + 3 * STEP / 8], [x + 3 * STEP / 4, y + 7 * STEP / 8]]);
			break;
		case PieceTypes.ROOK:
			drawPolygon([[x + STEP / 8, y + STEP / 8], [x + 2 * STEP / 5, y + STEP / 8], [x + 2 * STEP / 5, y + 2 * STEP / 5], [x + 3 * STEP / 5, y + 2 * STEP / 5], [x + 3 * STEP / 5, y + STEP / 8], [x + 7 * STEP / 8, y + STEP / 8], [x + 7 * STEP / 8, y + 7 * STEP / 8], [x + STEP / 8, y + 7 * STEP / 8]]);
			break;
		case PieceTypes.BISHOP:
			drawPolygon([[x + STEP / 8, y + 7 * STEP / 8], [x + STEP / 2, y + STEP / 4], [x + 7 * STEP / 8, y + 7 * STEP / 8]]);
			drawCircle(x + STEP / 2, y + 3 * STEP / 16, 1/16, 0, false);
			break;
		case PieceTypes.QUEEN:
			drawPolygon([[x + STEP / 8, y + STEP / 4],[x + STEP / 2, y + STEP /2], [x + 7 * STEP / 8, y + STEP / 4], [x + 7 * STEP / 8, y + 7 * STEP / 8], [x + STEP / 8, y + 7 * STEP / 8]]);
			drawCircle(x, y, 3/16, STEP / 2, false);
			drawCircle(x + STEP / 4, y + 3 * STEP / 16, 1/16, 0);
			drawCircle(x + 3 * STEP / 4, y + 3 * STEP / 16, 1/16, 0);
			break;
		default:
			drawCircle(x, y, 3 / 8, STEP / 2, false);
			drawText(String(piece.type), x + 2 * STEP / 5, y + STEP / 2);
			break;
	}
}

// draw the basic grid
function draw(){
	ctx.fillStyle = "";
	ctx.strokeStyle = "#000000";
	ctx.lineWidth = 2.0;
	
	for(var i = 0; i < LINES; i++){
		drawLine(MIN, MIN+i*STEP, MAX, MIN+i*STEP);
		drawLine(MIN+i*STEP, MIN, MIN+i*STEP, MAX);
	}
	
	redraw();
}

// draw the contents of the board
function redraw(){
	ctx.lineWidth = 2.0;
	ctx.fillStyle = "#ffffff";
	ctx.strokeStyle = "#000000";
	
	for(var i = 0; i < WIDTH; i++){
		for(var j = 0; j < HEIGHT; j++){
			drawSpace(i, j, "#ffffff");
			if(board[i][j].type != PieceTypes.EMPTY){
				drawPiece(i, j, board[i][j]);
			}
		}
	}
}