function CellularMessanger()
{
	this.socket			= null

	this.commandIdx 	= 0
	this.hashMap		= new Object()

	this.onnoconnect 	= null
	this.onconnect 		= null
}

CellularMessanger.prototype._commandIdFromNumber = function(number)
{
	return 'C'+String(number)
}

CellularMessanger.prototype.connect = function(ServerAddress)
{
	var parent = this

	this.socket = new WebSocket(ServerAddress)
	this.socket.onclose = this.onnoconnect
	this.socket.onopen	= this.onconnect

	this.socket.onmessage = function(d)
	{	
		response   		= d.data
		commandSplit    = String(response).split(' ')

		commandIdx 		=  Number.parseInt(commandSplit[0])
		commandType		=  String(commandSplit[1])

		if(commandType == 'OK')
			commandType = 0

		else if (commandType == 'ER')
			commandType = 1

		load = commandSplit.slice(2).join(' ')

		cmdId  = parent._commandIdFromNumber(commandIdx)
		toCall = parent.hashMap[cmdId][commandType]
		

		if (toCall)
			toCall(load)

		delete parent.hashMap[cmdId]
	}
}


CellularMessanger.prototype.issueCmd = function(cmd, callback_ok = null, callback_err = null)
{

	currCommandIdx = this.commandIdx++

	this.hashMap[this._commandIdFromNumber(currCommandIdx)] = [callback_ok, callback_err]

	reqArr = [String(currCommandIdx), cmd]
	request = reqArr.join(' ')
	this.socket.send(request)

	return currCommandIdx
}
