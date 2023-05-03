$(document).ready(function() {
    // send button click event handler
    $('button:contains("Send")').click(function() {
        var inputVal = $('.chat-input input').val();
        if (inputVal !== '') {
            $('.chat-log').append('<div class="chat-message"><span class="user">You:</span> ' + inputVal + '</div>');
            $('.chat-input input').val('');
        }
    });
    
    // history button click event handler
    $('button:contains("History")').click(function() {
        alert('Show chat history!');
    });
});
