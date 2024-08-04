/*price range*/

 $('#sl2').slider();

	var RGBChange = function() {
	  $('#RGB').css('background', 'rgb('+r.getValue()+','+g.getValue()+','+b.getValue()+')')
	};	
		
/*scroll to top*/

$(document).ready(function(){
	$(function () {
		$.scrollUp({
	        scrollName: 'scrollUp', // Element ID
	        scrollDistance: 300, // Distance from top/bottom before showing element (px)
	        scrollFrom: 'top', // 'top' or 'bottom'
	        scrollSpeed: 300, // Speed back to top (ms)
	        easingType: 'linear', // Scroll to top easing (see http://easings.net/)
	        animation: 'fade', // Fade, slide, none
	        animationSpeed: 200, // Animation in speed (ms)
	        scrollTrigger: false, // Set a custom triggering element. Can be an HTML string or jQuery object
					//scrollTarget: false, // Set a custom target element for scrolling to the top
	        scrollText: '<i class="fa fa-angle-up"></i>', // Text for element, can contain HTML
	        scrollTitle: false, // Set a custom <a> title if required.
	        scrollImg: false, // Set true to use image
	        activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
	        zIndex: 2147483647 // Z-Index for the overlay
		});
	});
});




function updatePrice(container, n) {
   //container -> each one of the $('.cd-gallery').children('li')
   //n -> index of the selected item in the .cd-item-wrapper
   var priceTag = container.find('.cd-price'),
       selectedItem = container.find('.cd-item-wrapper li').eq(n);
   if( selectedItem.data('sale') ) { 
      // if item is on sale - cross old price and add new one
      priceTag.addClass('on-sale');
      var newPriceTag = ( priceTag.next('.cd-new-price').length > 0 ) ? priceTag.next('.cd-new-price') : $('<em class="cd-new-price"></em>').insertAfter(priceTag);
      newPriceTag.text(selectedItem.data('price'));
      setTimeout(function(){ newPriceTag.addClass('is-visible'); }, 100);
   } else {
      // if item is not on sale - remove cross on old price and sale price
      priceTag.removeClass('on-sale').next('.cd-new-price').removeClass('is-visible').on('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(){
         priceTag.next('.cd-new-price').remove();
      });
   }
}

// support chatbox
document.addEventListener('DOMContentLoaded', function () {
	// chatbox
    const chatboxToggle = document.querySelector('.chatbox-toggle');
	const chatboxMessage = document.querySelector('.chatbox-message-wrapper');

	const chatboxForm = document.querySelector(".chatbox-message-form");

	const chatboxHeader = document.querySelector('.chatbox-message-header');
	const chatboxMessageContent = document.querySelector('.chatbox-message-content');
	const chatboxNoMessageContent = document.querySelector('.chatbox-message-no-message');
	const chatboxBottom = document.querySelector('.chatbox-message-bottom');

	const textarea = document.querySelector('.chatbox-message-input')
// loggin

	const loginWrapper = document.getElementById('login-wrapper');
	const otpWrapper = document.getElementById("otp-wrapper");
	const isAuthenticated = document.getElementById('is_authenticated').getAttribute('value') === 'True';
	console.log(isAuthenticated)
	if (isAuthenticated) {
		// If the user is logged in, hide the login and OTP forms
		const roomId = document.getElementById('room_data').getAttribute('data-room-id');
		const userName = document.getElementById('username').getAttribute('data-user-name');
		console.log(userName)
		loginWrapper.style.display = 'none';
		otpWrapper.style.display = 'none';
		chatboxHeader.style.display = 'block';
		chatboxNoMessageContent.style.display = 'block';
		chatboxBottom.style.display = 'block';
		
		textarea.addEventListener("input" , function () {
			// we set that the input row doesn't have to cross 6 rows
			let line = textarea.value.split("\n").length;
		
			if(textarea.rows < 6 || line < 6){
				textarea.rows = line
			}
		
			// we set style for when the rows of the input is more then 1 row
			if(textarea.rows > 1){
				chatboxForm.style.alignItems = "flex-end"
			}else{
				chatboxForm.style.alignItems = "center   "
			}
		})

		function scrollBottom(){
			chatboxMessageContent.scrollTo(0 , chatboxMessageContent.scrollHeight); // we use this function for when we send a message , the container automaticlly goes at the bottom
		}

		function isValid(value){
			let text = value.replace(/\n/g , "")
			text = text.replace(/\s/g , "");
			
			return text.length > 0
		}

		function writeMessage(data){

			var athor = data['__str__'];
			var command = data['command']
			var timestamp = data['timestamp']

			function addZero(num){
				return num < 10 ? "0" + num : num
			}
			
			function formatTimestamp(timestamp) {
				const date = new Date(timestamp); // Converts the timestamp string to a Date object
				const hours = addZero(date.getHours());
				const minutes = addZero(date.getMinutes());
				return `${hours}:${minutes}`;
			}
			
			const messageClass = athor === userName ? 'sent' : 'received';

			// the user message
			let message = `
				<div class="chatbox-message-item ${messageClass}"> 
					<span class="chatbox-message-item-text"> 
						${data.text.trim().replace(/\n/g , "<br>\n")}
					</span>
					<span class="chatbox-message-item-time">${formatTimestamp(timestamp)}</span> 
				</div>
		`
			chatboxMessageContent.insertAdjacentHTML('beforeend' , message);
			chatboxForm.style.alignItems = "center" // put the textes at the middle
			textarea.rows = 1 // get the row of the input back to 1
			textarea.focus(); // after the sending the message , focus on the input
			textarea.value = ""; // empty the input value
			chatboxNoMessageContent.style.display = "none";
			scrollBottom()
		}


		chatboxToggle.addEventListener("click" , function(){
			chatboxMessage.classList.toggle('show');
			
			const chatSocket = new ReconnectingWebSocket(
				'ws://'
				+ window.location.host
				+ '/ws/chat/'
				+ roomId + '/'
			);
	
			chatSocket.onopen = function() {
				chatSocket.send(JSON.stringify(
					{ 
						'command': 'fetch_message',
						'room_id':roomId
					}
				));
			};

			chatboxForm.addEventListener("submit" , function(e){
				e.preventDefault() // stopping the page from refreshing
				if(isValid(textarea.value)){
					chatSocket.send(JSON.stringify({
						'message':textarea.value,
						'command':'new_message',
						'username': userName,
						'room_id':roomId
					}))
					// writeMessage()
				}
			})

			chatSocket.onmessage = function(e){
				var data = JSON.parse(e.data);
				if (data['command'] === 'fetch_message'){
					console.log(data)
					for (let i=data['message'].length-1; i>=0 ; i--){
					writeMessage(data['message'][i]);
					}
				}
				else if (data['command'] === "new_message" ){
					console.log(data)
					writeMessage(data);
				}

			};

			chatSocket.onclose = function() {
				console.log('WebSocket connection clossed.');
			};


		});
    } else {
        // If the user is not logged in
		loginWrapper.style.display = 'block';
		chatboxHeader.style.display = 'none';
     	chatboxBottom.style.display = 'none';
        chatboxNoMessageContent.style.display = 'none';
	
		chatboxToggle.addEventListener("click" , function(){
			chatboxMessage.classList.toggle('show');

			$(document).on('submit','#login-from',function(e){
				e.preventDefault();
				
				$.ajax({
					type:'POST',
					url:'/chatbox-email/',
					data:{
						email:$('#login-input').val(),
						csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
					},
					success:function(data){
						$('#login-wrapper').hide()
						$('#otp-wrapper').show()

						const otpInputs = document.querySelectorAll(".otp__conversation-input")
						
						otpInputs.forEach((input , index1) => {
							input.addEventListener("keyup" , function(e){
								const currentInput = input,
								nextInput = input.nextElementSibling,
								prevInput = input.previousElementSibling;
							
								if(currentInput.value.length > 1){
									currentInput.value = "";
									return;
								}

								if(nextInput && nextInput.hasAttribute("disabled") && currentInput.value !== ""){
									nextInput.removeAttribute("disabled");
									nextInput.focus()
								}

								if (e.key === "Backspace"){
									otpInputs.forEach((input , index2) => {
										if(index1 <= index2 && prevInput){
											input.setAttribute("disabled" , true);
											currentInput.value = "";
											prevInput.focus()
										}
									})
								}
							})
						})

						window.addEventListener("load" , function(){
							otpInputs[0].focus()
						})
						
					},
					error: function(xhr, status, error) {
						// Handle any errors that occur during the request
						console.error("AJAX Error: ", status, error);
					}
				})
			})

			$(document).on('submit','#otp-form',function(e){
				e.preventDefault();
				
				const otpInputs = document.querySelectorAll(".otp__conversation-input");
				const otpValues = Array.from(otpInputs).map(input => input.value).join("");

				$.ajax({
					type:'POST',
					url:'/chatbox-otp/',
					data:{
						email:$('#login-input').val(),
						otp:otpValues,
						csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
					},
					success:function(data){
						location.reload()
					},
					error: function(xhr, status, error) {
						// Handle any errors that occur during the request
						console.error("AJAX Error: ", status, error);
					}
				})
			})
		});
    };
});

// support_pannel_view
