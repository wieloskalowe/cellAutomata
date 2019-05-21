function Grid(DivGridNode)
{
	this.CELL_WIDTH  = 50
	this.CELL_HEIGHT = 50
	this.xs = 0
	this.ys = 0

	this.divGridNode = DivGridNode
	this.mousedown = false
	this.cellsData = []
	this.oncelltoggle = null // function(cellReference, dataIndex, toggled)


}


Grid.prototype._updateMainTextPos = function(cell)
{
	let parent = cell.parentNode

	let main = getChildByClassName(cell.parentNode, '.main-cell-text')
	let bbm = main.getBBox()
	let bbc = parent.getBBox()
	main = d3.select(main)



	main.attr('x', bbc.x+bbc.width/2-bbm.width/2)
	main.attr('y', bbc.y+bbc.height/2-bbm.height/(parent.subText ? 3 : -4))
}

Grid.prototype._updateSubTextPos = function(cell)
{
	let parent = cell.parentNode

	let sub = getChildByClassName(cell.parentNode, '.sub-cell-text')
	let bbs = sub.getBBox()
	let bbc = parent.getBBox()
	sub = d3.select(sub)

	sub.attr('x', bbc.x+bbc.width/2-bbs.width/2)
	sub.attr('y', bbc.y+bbc.height/2+bbs.height)

}

Grid.prototype._appendCells = function(x,y, modifiable, CellsData, CellsProps)
{

	var parent = this;
	var main_group = d3.select(this.divGridNode).select('#g4')

	this.cellsData = this.cellsData.concat(CellsData)

	var f =  function(d) {
		   if(!parent.mousedown)return;

		   let toggled = !JSON.parse(this.getAttribute('toggled'))
		   this.setAttribute('toggled',  JSON.stringify(toggled))

		   if(parent.oncelltoggle)
		   	parent.oncelltoggle(this, d.dataIndex, toggled)
	    }

	var f2 = function(d) {

		  let toggled = !JSON.parse(this.getAttribute('toggled'))
		   this.setAttribute('toggled',  JSON.stringify(toggled))

		   if(parent.oncelltoggle)
		   	parent.oncelltoggle(this, d.dataIndex, toggled)
	    }



	var data = new Array();
	let idx = this.xs*this.ys
	let prop_idx = 0;
	let creation = idx == 0 ? true : false;

	let CELL_WIDTH  =  this.CELL_WIDTH ; //TODO
	let CELL_HEIGHT =  this.CELL_HEIGHT; //TODO

	let xpos = 1
	let ypos = this.ys*CELL_HEIGHT

	
	// iterate for rows	
	for (var row = 0; row < y; row++) {
		data.push( new Array() );
		
		// iterate for cells/columns inside rows
		for (var column = 0; column < x; column++) {

			let o = {
				x: xpos,
				y: ypos,
				width:  CELL_WIDTH,
				height: CELL_HEIGHT,
				mainText: null,
				subText:  null,
				fill: 	"#ffffff", 
				dataIndex: idx
			}

			if(Array.isArray(CellsProps) && prop_idx < CellsProps.length )
			{
				o.mainText = CellsProps[prop_idx]['mainText']
				o.subText  = CellsProps[prop_idx]['subText']
				o.fill  = CellsProps[prop_idx]['fill'] || o.fill
			}
			data[row].push(o)
			
			xpos +=  CELL_WIDTH;
			idx++;
			prop_idx++;
		}
		
		xpos = 1;
		ypos += CELL_HEIGHT;	
	}


	if (creation)
	{
		var row = main_group.selectAll(".row");
		var row_g = row.data(data)
					.enter()
					.append("g")
					.attr("class", "row")
					.attr("modifiable", JSON.stringify(modifiable))
	}
	else
	{
		var row_g = main_group
				.data(data)
				.append("g")
				.attr('class', 'row')
				.attr("modifiable", JSON.stringify(modifiable))
	}




	var column = row_g.selectAll(".square")
		.data(function(d) { return d; })
		.enter()
		.append("g")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.attr("class", "text-group")
		.append("rect")
		.attr("class","square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.attr("toggled", "false")
		.style("fill", function(d) { return d.fill; } )
		.style("stroke", "#222")
		.on('mouseover',f).on('mousedown', f2);



	row_g.selectAll(".text-group")
		.data(function(d) { return d; })
		.append("text")
		.attr("class", ".sub-cell-text")
		.text(function(d){this.parentNode.subText = (d.subText != null && d.subText.length > 0); return d.subText;})
		.attr("font-size", "12")
		.attr("font-family", "Calibri")
		.attr("x", function(d){return d.x+d.width/2-this.getBBox().width/2;})
		.attr("y", function(d){return d.y+d.height/2+this.getBBox().height;})
		.attr("fill", "red")
		.style('paint-order','stroke')
		.style('stroke','#eeeeee')
		.style('stroke-width','2px')
		.style('stroke-linecap','butt')
		.style('stroke-linejoin','miter')
		.attr('fill', '#999999')


	//main text
	row_g.selectAll(".text-group")
		.data(function(d) { return d; })
		.append("text")
		.attr("class", ".main-cell-text")
		.text(function(d){return d.mainText;})
		.attr("font-size", "12")
		.attr("font-family", "Calibri")
		.attr("font-weight", "bold")
		.attr("x", function(d){return d.x+d.width/2-this.getBBox().width/2;})
		.attr("y", function(d){return d.y+d.height/2-this.getBBox().height/(this.parentNode.subText ? 3 : -4);})
		.style('paint-order','stroke')
		.style('stroke','#ffffff')
		.style('stroke-width','2px')
		.style('stroke-linecap','butt')
		.style('stroke-linejoin','miter')
		.attr('fill', '#000000')

	row_g.selectAll(".text-group")
		.data(function(d) { return d; })
		.append("rect")
		.attr("class", ".front-square")
		.attr("x", function(d) { return d.x; })
		.attr("y", function(d) { return d.y; })
		.attr("width", function(d) { return d.width; })
		.attr("height", function(d) { return d.height; })
		.style("fill", "#222")
		.attr("fill-opacity", "0")
		.style("stroke", "rgba(0,0,0,0)")
		.on("mousedown", function(d){ 
			  let modifiable = d3.select(this.parentNode.parentNode).attr('modifiable')

			  if(!JSON.parse(modifiable))return
			  if (event.button != 0) return

			  var evt = new MouseEvent("mousedown");
			  evt.button = 0;
			  d3.select(this.parentNode).select('.square').node().dispatchEvent(evt);
			 
			})
		.on('mouseover', function(d){ 

			  let modifiable = d3.select(this.parentNode.parentNode).attr('modifiable')
				
			  if(!JSON.parse(modifiable))return

			  if (event.button != 0)return

			  var evt = new MouseEvent("mouseover");
			  d3.select(this.parentNode).select('.square').node().dispatchEvent(evt);
			 
		  });

		
		this.ys++;



}

function getChildByClassName(element, className)
{
	
	for(let n = 0; n<element.children.length; n++)
		for(let l =0; l<element.children[n].classList.length; l++)
		if(element.children[n].classList[l] === className)
			return element.children[n]


	return undefined
}

Grid.prototype.clear = function()
{
	this.CELL_WIDTH  = 50
	this.CELL_HEIGHT = 50
	this.xs = 0
	this.ys = 0

	this.mousedown = false
	this.cellsData = []

	d3.select(this.divGridNode).node().innerHTML=''
}

Grid.prototype.updateSubText = function(cell, text)
{
	let sub = d3.select(cell.parentNode).select('.sub-cell-text')
	sub = d3.select(  getChildByClassName(cell.parentNode, '.sub-cell-text') )
	sub.text(text)



	cell.parentNode.subText = ((text) || text.length > 0);
	this._updateMainTextPos(cell)
	

	this._updateSubTextPos(cell)
 

}


Grid.prototype.setModifiableByRow = function(row, modifiable)
{
	row = d3.select(row) 
	row.attr('modifiable', JSON.stringify(modifiable))
}

Grid.prototype.setModifiableByRowIdx = function(rowIdx, modifiable)
{
	rows = this.divGridNode.getElementsByClassName('row')
	row = rows[rowIdx]


	this.setModifiableByRow(row, modifiable)

}


Grid.prototype.cellXYtoIdx = function(x,y)
{
	if(y >= this.ys)
	{	
		debugger;
		throw('Y index is too large!')
	}

	if(x >= this.xs)
	{
		debugger;
		throw('X index is too large!')
	}

	let idx = y*this.xs + x

	return parseInt(idx);
}

Grid.prototype.cellIdxtoXy = function(Idx)
{
	if(Idx < 0)
		throw('Cannot convert idx to x,y, index cannot be below 0!')

	if(Idx >= this.xs*this.ys )
		throw('Cannot convert idx to x,y, index is to great!')


	// x x x
	// x x x
	// x x x
 	// x x x

 	
 	let yp = Math.floor(Idx/this.xs)
 	let xp = Idx - (this.xs*yp)
 	let ret = {x:xp, y:yp}
	return ret
}

Grid.prototype.toggleCell = function(cellIdx)
{


	if (this.xs == 0 && this.ys == 0)
		throw('Cannot toggle cell, grid is empty!')

	let sizeX = this.xs > 0 ? this.xs : 1
	let sizeY = this.ys > 0 ? this.ys : 1

	if(cellIdx >= (sizeX * sizeY))
		throw('Cannot toggle cell, index out of bound!')



	let sqrs = document.getElementsByClassName('square');
	if(cellIdx >= sqrs.length )
		throw('Cannot toggle cell, number of squares is too small, somehow...')

	if(!sqrs)
		throw('Cannot toggle cell, sqrs is null?')

	var evt = new MouseEvent("mousedown");
	evt.button = 0;
	sqrs[cellIdx].dispatchEvent(evt);
}

Grid.prototype.toggleCellXY = function(x,y)
{

	this.toggleCell(this.cellXYtoIdx(x,y));
}



Grid.prototype.updateCellsProps = function(props)
{
	if (this.xs == 0 && this.ys == 0)
		throw("Cannot update cell's properities in empty grid!")

	let sizeX = this.xs > 0 ? this.xs : 1
	let sizeY = this.ys > 0 ? this.ys : 1

	if(props.length > (sizeX * sizeY))
		throw("Cannot update cell's properities, to much cell's specified!")

	let sqrs = document.getElementsByClassName('square');
	if(props.length  > sqrs.length )
		throw("Cannot update cell's properities, number of squares is too small, somehow...")

	if(!sqrs)
		throw("Cannot update cell's properities, sqrs is null?")

	for(let n=0; n<props.length; n++)
	{

		if(props[n]['fill'])
			sqrs[n].style.fill = props[n]['fill']

		if( props[n]['subText'] && typeof(props[n]['subText']) != typeof('') )
			this.updateSubText(sqrs[n], props[n]['subText'])

		if( props[n]['mainText'] && typeof(props[n]['mainText']) != typeof('') )
			this.updateMainText(sqrs[n], props[n]['mainText'])
	}

}

Grid.prototype.updateCellProps = function(idx, props)
{
	if (this.xs == 0 && this.ys == 0)
		throw("Cannot update cell's properities in empty grid!")

	let sizeX = this.xs > 0 ? this.xs : 1
	let sizeY = this.ys > 0 ? this.ys : 1

	let sqrs = document.getElementsByClassName('square');

	if(idx < 0)
		throw("Cannot update cell's properities, index cannot be negative!")

	if(idx > sizeX*sizeY)
		throw("Cannot update cell's properities, index out of range!")

	if(!sqrs)
		throw("Cannot update cell's properities, sqrs is null?")

	sqrs = sqrs[idx];

		if(props['fill'])
			sqrs.style.fill = props['fill']

		if( props['subText'] && typeof(props['subText']) != typeof('') )
			this.updateSubText(sqrs, props['subText'])

		if( props['mainText'] && typeof(props['mainText']) != typeof('') )
			this.updateMainText(sqrs, props['mainText'])
	

}

Grid.prototype.setCellState = function(cellIdx, state)
{
	
}


Grid.prototype.updateMainText = function(cell, text)
{
	let main = d3.select(cell.parentNode).select('.main-cell-text')
	main = d3.select(  getChildByClassName(cell.parentNode, '.main-cell-text') )
	main.text(text)


	this._updateMainTextPos(cell)
 }

Grid.prototype.appendRow = function(modifiable = true, CellsData=[], CellsProps=[])
{
	this._appendCells(this.xs, 1, modifiable, CellsData, CellsProps)
}


Grid.prototype.newGrid = function(x,y, modifiable = true, CellsData=[], CellsProps=[], translateX = 0, translateY=0)
{
	this.clear();


	if(typeof(this.divGridNode) === "string")
		this.divGridNode = d3.select(this.divGridNode).node()



	
	var parent = this;

	var grid = d3.select(this.divGridNode)
		.append("svg")
		.style("width","100%").style("height","100%")
		.attr("id", 'grid-svg')
		.append("g")
		.attr("id", "g4")
		.attr("fill", "none")
		.attr('transform', 'translate('+translateX+', '+translateY+')')
		

	this._appendCells(x,y, modifiable, [], CellsProps)

	this.cellsData = CellsData;
	this.xs = x
	this.ys = y

	var g4 = document.getElementById('g4')
	var instance = panzoom(g4);

	 d3.select("#grid").on("mousedown",   function(){ if(event.button == 0){instance.pause(); parent.mousedown=true}});
	 d3.select("#grid").on("mouseup",     function(){ if(event.button == 0){instance.resume(); parent.mousedown=false}});

}