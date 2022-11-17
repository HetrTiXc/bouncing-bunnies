import { Application, Sprite, Graphics, Text, TextStyle } from 'pixi.js'

const app = new Application({
	view: document.getElementById("pixi-canvas") as HTMLCanvasElement,
	resolution: window.devicePixelRatio || 1,
	autoDensity: true,
	backgroundColor: 0x6495ed,
	width: 640,
	height: 700
});

class Block {
	left: number;
	top: number;
	right: number;
	bottom: number;
	status: number;

    constructor(left: number, top: number, right: number, bottom: number, status: number) {
        this.left = left;
        this.top = top;
        this.right = right;
        this.bottom = bottom;
        this.status = status;
	}
}

interface Board {
	cells: blockObjects[];
}

interface blockObjects {
	x: number;
	y: number;
	bottom: number;
	left: number;
	top: number;
	right: number;
	status: number;
}

const fetchBoard = async () => {
	let response = await fetch('http://localhost:8001/map', {
		method: 'POST',
		headers: {
			'content-type': 'application/json;charset=UTF-8'
		},
		body: JSON.stringify({
			seed: 1,
		}),
	});
	let data = await response.json();
	if (response.ok) {
		return data;
	} else {
		console.error("Failed to receive board");
		return "{}"
	}
}

const fetchShortestPath = async () => {
	let response = await fetch('http://localhost:8001/shortestPath', {
		method: 'POST',
		headers: {
			'content-type': 'application/json;charset=UTF-8'
		},
		body: JSON.stringify({
			seed: 1,
		}),
	});
	let data = await response.json();
	if (response.ok) {
		return data;
	} else {
		console.error("Failed to receive shortest path");
		return ""
	}
}

fetchBoard().then(result => {
	let parsedJson = result as Board;
	for(let i = 0; i < parsedJson.cells.length; i++) {
		console.log(i);
		let cell = parsedJson.cells[i];
		let block = new Block(cell.left, cell.top, cell.right, cell.bottom, cell.status);

	// for (let x = 0; x < board.length; x++) {
	// 	for (let y = 0; y < board.length; y++) {

		let x = cell.x;
		let y = cell.y;
		const bunny: Sprite = Sprite.from("bunny.png");

		bunny.anchor.set(0.5);
		let shortestSide = app.screen.width < app.screen.height ? app.screen.width : app.screen.height;
		let scale = shortestSide/Math.sqrt(parsedJson.cells.length)
		bunny.x = scale * x + scale/2
		bunny.y = scale * y + scale/2

		// Opt-in to interactivity
		bunny.interactive = true;

		// Shows hand cursor
		bunny.buttonMode = true;

		// Pointers normalize touch and mouse
		bunny.on('pointerdown', onClick);

		app.stage.addChild(bunny);

		function onClick() {
			bunny.scale.x *= 1.25;
			bunny.scale.y *= 1.25;
		}
		if (block.left == 1) {
			let line = new Graphics();
			let thickness = 4;

			line.position.set(bunny.x - scale/2, bunny.y - scale/2);

			// Draw the line (endPoint should be relative to myGraph's position)
			line.lineStyle(thickness, 0xffffff)
				.moveTo(0, 0)
				.lineTo(0, scale);
			
			app.stage.addChild(line)
		}

		if (block.top == 1) {
			let line = new Graphics();
			let thickness = 4;

			line.position.set(bunny.x - scale/2, bunny.y - scale/2);

			// Draw the line (endPoint should be relative to myGraph's position)
			line.lineStyle(thickness, 0xffffff)
				.moveTo(0, 0)
				.lineTo(scale, 0);
			
			app.stage.addChild(line)
		}

		if (block.right == 1) {
			let line = new Graphics();
			let thickness = 4;

			line.position.set(bunny.x + scale/2, bunny.y - scale/2);

			// Draw the line (endPoint should be relative to myGraph's position)
			line.lineStyle(thickness, 0xffffff)
				.moveTo(0, 0)
				.lineTo(0, scale);
			
			app.stage.addChild(line)
		}

		if (block.bottom == 1) {
			let line = new Graphics();
			let thickness = 4;

			line.position.set(bunny.x - scale/2, bunny.y + scale/2);

			// Draw the line (endPoint should be relative to myGraph's position)
			line.lineStyle(thickness, 0xffffff)
				.moveTo(0, 0)
				.lineTo(scale, 0);
			
			app.stage.addChild(line)
		}
	}
	// 	}
	// }
});

fetchShortestPath().then(result => {
	const style = new TextStyle({
		fontFamily: 'Arial',
		fontSize: 30,
		fill: ['#ffffff'], // gradient
		stroke: '#000000',
		strokeThickness: 5,
	});
	const basicText = new Text('Shortest path: ' + result, style);
	basicText.x = 10;
	basicText.y = app.screen.height - 50;

	app.stage.addChild(basicText);
});

//let board = getBoard().then(res => { return res as Board });

// const bunny: Sprite = Sprite.from("bunny.png");

// bunny.anchor.set(0.5);

// bunny.x = app.screen.width / 2;
// bunny.y = app.screen.height / 2;