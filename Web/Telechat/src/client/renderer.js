const socket = io(window.electron.api_url);


const conversationList = document.getElementById('conversation-list');
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendMessageButton = document.getElementById('send-message');

let conversations = [];
let currentConversation = null;
let aiBotCounter = 1;
const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;

function createConversation(name, conv_uuid = undefined) {
    let is_report = 0;
    if (name === 'AIBot') {
        const existingConvo = conversations.find(convo => convo.name.startsWith('AIBot'));
        if (existingConvo) {
            name = `AIBot - ${aiBotCounter++}`;
        }
    } else if (name === 'ReportBot') {
        const existingConvo = conversations.find(convo => convo.name === 'ReportBot');
        if (existingConvo) {
            selectConversation(existingConvo.id);
            return;
        }
        is_report = 1;
    } else {
        name = name;
    }
    let conversation = {
        id: crypto.randomUUID(),
        name: name,
        messages: []
    }
    if(name !== "BOT REVIEW") {
        conversation["report"] = is_report;
    } else {
        currentConversation = conversation;
        let socket_bot = io('http://localhost:3000/',{
            path: "/reviews/"+conv_uuid+"/" 
        });
        socket_bot.on('response', (data) => {
            if(data !== undefined) {
                if(data !== "END REVIEW") {
                    let current_message = data.split(": ");
                    if(current_message[0] == "USER"){
                        currentConversation.messages.push({bot: 0, message: current_message[1]})
                    } else {
                        currentConversation.messages.push({bot: 1, message: current_message[1]})
                    }
                } else {
                    currentConversation.messages.push({bot: 1, message: "<button id='download' onclick='screenshot()'>Download conversation screenshot</button>"});
                }
            }
        });
        conversation["report"] = conv_uuid;
    }
    document.getElementById('message-container').style.display = 'block';
    conversations.push(conversation);
    renderConversations(true);
    selectConversation(conversation.id);
}

function screenshot() {
    const element = document.getElementById('messages');
    html2canvas(element).then(function(canvas) {
        const image = canvas.toDataURL('image/png');

        const link = document.createElement('a');
        link.href = image;
        link.download = 'capture.png';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
}

function renderConversations(first_render) {
    conversationList.innerHTML = '';

    const addConversationButton = document.createElement('button');
    addConversationButton.textContent = '+';
    addConversationButton.onclick = () => showAddConversationMenu(addConversationButton);
    addConversationButton.style.display = 'block';
    addConversationButton.style.margin = '10px';
    conversationList.appendChild(addConversationButton);

    if (conversations.length === 0) {
        const noConversationMessage = document.createElement('div');
        noConversationMessage.className = 'no-conversation';
        noConversationMessage.textContent = 'Aucune conversation 😢';
        noConversationMessage.style.textAlign = 'center';
        noConversationMessage.style.marginTop = '20px';
        conversationList.appendChild(noConversationMessage);
        return;
    }

    conversations.forEach(convo => {
        const convoDiv = document.createElement('div');
        convoDiv.className = 'conversation';
        convoDiv.innerHTML = `
            <div>${convo.name}</div>
            <div style="font-size: 12px; color: #666;">${convo.id}</div>
        `;
        convoDiv.onclick = () => selectConversation(convo.id);

        if (currentConversation && convo.id === currentConversation.id) {
            convoDiv.classList.add('active-conversation');
            if(first_render) {
                setTimeout(() => {document.getElementsByClassName("active-conversation")[0].click();test=0;},200);
            }
        } else {
            convoDiv.classList.remove('active-conversation');
        }
        conversationList.appendChild(convoDiv);
    });
}

function showAddConversationMenu(addConversationButton) {
    const menu = document.createElement('div');
    menu.className = 'menu';
    menu.style.position = 'absolute';
    menu.style.backgroundColor = 'white';
    menu.style.border = '1px solid #ccc';
    menu.style.padding = '10px';
    menu.style.zIndex = 1000;

    const aiBotButton = document.createElement('button');
    aiBotButton.textContent = 'AIBot';
    aiBotButton.className = 'menu-button';
    aiBotButton.onclick = () => {
        createConversation('AIBot');
        removeMenu();
    };
    menu.appendChild(aiBotButton);

    const reportBotButton = document.createElement('button');
    reportBotButton.textContent = 'ReportBot';
    reportBotButton.className = 'menu-button';
    reportBotButton.onclick = () => {
        createConversation('ReportBot');
        removeMenu();
    };
    menu.appendChild(reportBotButton);

    document.body.appendChild(menu);

    const rect = addConversationButton.getBoundingClientRect();
    menu.style.top = `${rect.bottom}px`;
    menu.style.left = `${rect.left}px`;

    function removeMenu() {
        document.body.removeChild(menu);
    }

    function handleClickOutside(event) {
        if (!menu.contains(event.target) && event.target !== addConversationButton) {
            removeMenu();
        }
    }

    document.addEventListener('click', handleClickOutside);

    function cleanup() {
        document.removeEventListener('click', handleClickOutside);
    }

    function closeMenu() {
        removeMenu();
        cleanup();
    }

    const originalRemoveMenu = removeMenu;
    removeMenu = () => {
        originalRemoveMenu();
        cleanup();
    };

    aiBotButton.onclick = () => {
        createConversation('AIBot');
        closeMenu();
    };

    reportBotButton.onclick = () => {
        createConversation('ReportBot');
        closeMenu();
    };
}

function selectConversation(id) {
    currentConversation = conversations.find(convo => convo.id === id);
    renderMessages();
    renderConversations(false);
}

function renderMessages() {
    if (!currentConversation) return;
    messagesDiv.innerHTML = '';
    currentConversation.messages.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message-bubble';
        msgDiv.innerHTML = msg.message;

        if (msg.bot) {
            msgDiv.classList.add('bot-message');
        } else {
            msgDiv.classList.add('user-message');
        }

        messagesDiv.appendChild(msgDiv);
    });
}

sendMessageButton.onclick = () => {
    sendMessage();
};

function sendMessage() {
    if (currentConversation && messageInput.value) {
        if(currentConversation.report == 1 && !uuidRegex.test(messageInput.value)) {
            alert("You must provide here the conversation UUID you want to report.");
            return;
        } else {
            socket.emit('message', {uuid: currentConversation.id, message: messageInput.value, report: currentConversation.report});
        }

        currentConversation.messages.push({bot: 0, message: messageInput.value});
        messageInput.value = '';
        renderMessages();
    }
}

window.electron.activate_check((res) => {
    if(res) {
        setInterval(function(){
            window.electron.check((data) => {
                createConversation("BOT REVIEW", data);
            });
        },1000) 
    }
})

messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

socket.on('response', (data) => {
    if (currentConversation) {
        currentConversation.messages.push({bot: 1, message: data});
        renderMessages();
    }
});

renderConversations(false);