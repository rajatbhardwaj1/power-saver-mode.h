import React, { useState } from 'react';
import data from './data.js';
import './chat.css';

function ChatBox() {
  const messages = data;
  const name = 'Rajat';

  const [newMessage, setNewMessage] = useState('');

  const handleNewMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSendMessage = () => {
    if (newMessage.trim() !== '') {
      const newMessageObj = { text: newMessage.trim(), by: 'sender' };
      setNewMessage('');
      messages.push(newMessageObj);
    }
  };

  return (
    <div className="chat-box">
      <div className="chat-box-header">{name}</div>
      <div className="chat-box-body">
        {messages.map((message, index) => (
          <div key={index} className={message.by === 'sender' ? 'chat-bubble sent' : 'chat-bubble received'}>
            {message.message}
          </div>
        ))}
      </div>
      <div className="chat-box-footer">
        <input type="text" value={newMessage} onChange={handleNewMessageChange} placeholder="Type your message..." />
        <button onClick={handleSendMessage}><i className="fa fa-send"></i></button>
      </div>
    </div>
  );
}

export default ChatBox;
