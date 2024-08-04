document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.querySelector('.form-control.type_msg')
    const button = document.querySelector('.input-group-text.send_btn')

    const currentRoomId = document.getElementById('room_data').getAttribute('data-room-id');
    const userName = document.getElementById('username').getAttribute('data-user-name');


    textarea.addEventListener("input" , function () {
        // we set that the input row doesn't have to cross 6 rows
        let line = textarea.value.split("\n").length;

        if(textarea.rows < 6 || line < 6){
            textarea.rows = line
        }

        // we set style for when the rows of the input is more then 1 row
        if(textarea.rows > 1){
            textarea.style.alignItems = "flex-end"
        }else{
            textarea.style.alignItems = "center   "
        }
    })

    function isValid(value){
        let text = value.replace(/\n/g , "")
        text = text.replace(/\s/g , "");
        
        return text.length > 0
    }

    function scrollBottom(body){
        body.scrollTo(0 , body.scrollHeight); // we use this function for when we send a message , the container automaticlly goes at the bottom
    }


    function writeMessage(data) {
        var author = data['__str__'];
        var is_superuser = data['is_superuser']; 
        console.log(is_superuser)// Corrected from "athor" to "author"
        var command = data['command'];
        var timestamp = data['timestamp'];
    
        function addZero(num) {
            return num < 10 ? "0" + num : num;
        }
    
        function formatTimestamp(timestamp) {
            const date = new Date(timestamp); // Converts the timestamp string to a Date object
            const hours = addZero(date.getHours());
            const minutes = addZero(date.getMinutes());
            return `${hours}:${minutes}`;
        }
    
        let message = ''; // Declare the message variable once
    
        // Determine the message content based on the author
        if (is_superuser === true) {
            message = `
                <div class="d-flex justify-content-end mb-4">
                    <div class="msg_cotainer_send">
                        ${data.text.trim().replace(/\n/g , "<br>\n")}
                        <span class="msg_time_send">${formatTimestamp(timestamp)}</span>
                    </div>
                </div>
            `;
        } else {
            message = `
                <div class="card-body msg_card_body">
                    <div class="d-flex justify-content-start mb-4">
                        <div class="msg_cotainer">
                            ${data.text.trim().replace(/\n/g , "<br>\n")}
                            <span class="msg_time">${formatTimestamp(timestamp)}</span>
                        </div>
                    </div>
                </div>
            `;
        }
    
        const body = document.querySelector('.card-body.msg_card_body');
        
        body.insertAdjacentHTML('beforeend', message);
        textarea.rows = 1; // get the row of the input back to 1
        textarea.focus(); // after sending the message, focus on the input
        textarea.value = ""; // empty the input value
        scrollBottom(body)
    }


    const chatSocket = new ReconnectingWebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + currentRoomId + '/'
    );

    chatSocket.onopen = function() {
        chatSocket.send(JSON.stringify(
            { 
                'command': 'fetch_message',
                'room_id':currentRoomId,
                'username':userName
            }
        ));
    };

    button.addEventListener("click" , (e) =>{
        e.preventDefault() // stopping the page from refreshing
        if(isValid(textarea.value)){
            chatSocket.send(JSON.stringify({
                'message':textarea.value,
                'command':'new_message',
                'username': userName,
                'room_id':currentRoomId
            }))
        }
    })

    chatSocket.onmessage = function(e){
        var data = JSON.parse(e.data);
        if (data['command'] === 'fetch_message'){
            for (let i=data['message'].length-1; i>=0 ; i--){
            writeMessage(data['message'][i]);
            }
        }
        else if (data['command'] === "new_message" ){
            writeMessage(data);
        }

    };

    chatSocket.onclose = function() {
        console.log('WebSocket connection clossed.');
    };

});