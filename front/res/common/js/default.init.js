const ESTABLISHED 	= 0
const LOST 			= 1
const CONNECTING	= 2

const CellularServerAddress = 'ws://localhost:1337'


var CUSTOM_ON_CONNECT_CALLBACK = null


var grid = new Grid('#grid');
var messanger = new CellularMessanger();
pectin_setMessangerInstance(messanger);

messanger.onnoconnect = function(){
	ConnectionStatus = LOST
	grid.clear()
	updateConnectionInfo()
}

messanger.onconnect = function(){

	ConnectionStatus = ESTABLISHED
	connectionTimeoutId = null
	updateConnectionInfo()


	if(CUSTOM_ON_CONNECT_CALLBACK)
		CUSTOM_ON_CONNECT_CALLBACK()
}

var connectionTimeoutId = null
function connect()
{
	if(connectionTimeoutId)
		clearTimeout(connectionTimeoutId)

	ConnectionStatus = CONNECTING
	messanger.connect(CellularServerAddress)

	updateConnectionInfo()
}

function updateConnectionInfo(){
	const CONNECTING_IMG = './res/common/img/load.gif'
	const CONNECTING_MSG = 'Nawiązywanie połączenia z serwerem...'

	const LOST_IMG = './res/common/img/nope.png'
	const LOST_MSG = 'Serwer nie odpowiada (X_X)'
	const LOST_SUB_MSG = '<a href="#" onclick="connect()">Ponowna próba połączenia<a> za 7s.'

	if(ConnectionStatus == CONNECTING)
	{
		d3.select('#connect_bg').style('display', 'block')

		d3.select('#infoImg').node().src = CONNECTING_IMG
		d3.select('#infoMsg').node().innerText = CONNECTING_MSG
		d3.select('#subInfoMsg').node().innerText = ''
	}

	if(ConnectionStatus == LOST)
	{
		d3.select('#connect_bg').style('display', 'block')

		d3.select('#infoImg').node().src = LOST_IMG
		d3.select('#infoMsg').node().innerText = LOST_MSG
		d3.select('#subInfoMsg').node().innerHTML = LOST_SUB_MSG
		connectionTimeoutId = setTimeout(function(){
				  									connect()
				  								 }, 7000)
	}

	if(ConnectionStatus == ESTABLISHED)
	{
		d3.select('#connect_bg').style('display', 'none')
	}

}

connect()
var ConnectionStatus = CONNECTING




