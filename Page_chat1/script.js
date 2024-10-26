// var
var message=document.getElementById("message"),
send_message=document.getElementById("send_message"),
sond=document.querySelectorAll("#sond"),
menu=document.getElementById("menu"),
chats=document.querySelector(".chats"),
main_menu=document.querySelector(".main_menu"),
message_user=document.querySelector(".you"),
message_robot=document.querySelector(".robot"),
message_user_value="",t=300,speech_robot=false,
firt_message_robot_valid=false,request_chat_valid=false,message_user_copy,message_robot_copy
message_user_copy=message_user.cloneNode(true)
message_robot_copy=message_robot.cloneNode(true)
message_user.remove()
message_robot.remove()
// var

// Speech
function speech(text_speech){
    if(speech_robot){
    var speech= new SpeechSynthesisUtterance();
    speech.text= text_speech;
    window.speechSynthesis.speak(speech);
}
}
// Speech



// message_robot

function message_chat(text){
    var div_robot_send,
    new_message;
    div_robot_send=message_robot_copy.cloneNode(true)
    new_message=div_robot_send.lastElementChild
    new_message.innerHTML=text
    chats.appendChild(div_robot_send)
    request_chat_valid=true
    firt_message_robot_valid=false
}

// message_robot

// message_add_br
function add_br(text_add_br){
    var xhr=new XMLHttpRequest(),
    new_text="",rep="";
        xhr.open('GET', 'http://127.0.0.1/add_br/br.php?text_add_br='+text_add_br)
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                rep=xhr.responseText;
            }
        };
        xhr.send();
    if (rep==""){
        return text_add_br;
    }
    else{
        return xhr.responseText
    }
}
// message_add_br

// function menu
function main_menu_on_off(e){
    var etat=getComputedStyle(main_menu).display;
    var elem=menu.firstElementChild;
    elem.classList.toggle("fa-bars")
    elem.classList.toggle("fa-xmark")
    if(etat=="block"){
        main_menu.classList.toggle("main_menu_anim_off")
        main_menu.classList.toggle("main_menu_anim_on")
        setTimeout(()=>{
            main_menu.style.display="none";
        },2001)
    }
    else{
        main_menu.style.display="block";
        main_menu.classList.toggle("main_menu_anim_off")
        main_menu.classList.toggle("main_menu_anim_on")
    }
}

// function menu


// function button send_message
function send_user(e){
    var div_user_send,new_message
    e.preventDefault()
    if ((message.value.trim()!="")&&(message.value.trim()!=null)&&(message.value.trim()!="undefined")){
    //    message_user
        message_user_value=(message.value.trim())
        div_user_send=message_user_copy.cloneNode(true)
        new_message=div_user_send.firstElementChild
        new_message.innerHTML=add_br(message_user_value)
        chats.appendChild(div_user_send)
        chats.scrollTop=chats.scrollHeight
        message.value=""
        firt_message_robot_valid=true
    //    message_user
    }

}
function firt_message_robot(e){
    if (firt_message_robot_valid){
        setTimeout(()=>{
           message_chat("Veuillez patienter");
           chats.scrollTop=chats.scrollHeight
           speech("Veuillez patienter");
        },t)
    }
}
function chat_error(e){
    var rep="Desolé,impossible d'atteindre le serveur Chatbot veuillez réessayer ultérieurement";
    var last_sms_robot=chats.lastElementChild.remove()
    message_chat(rep)
    chats.scrollTop=chats.scrollHeight
    speech(rep)
}
function request_chat(e){
    setTimeout(()=>{
        var fromData=new FormData()  
        fromData.append("message",message_user_value)  
        xhr=new XMLHttpRequest()
        xhr.open('POST', 'http://192.168.35.230:5000/chat');
        xhr.timeout=10000;
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
            var rep=xhr.responseText;
            var last_sms_robot=chats.lastElementChild.remove()
            message_chat(rep)
            chats.scrollTop=chats.scrollHeight
            speech(rep)
            }
        };
       xhr.addEventListener("error",chat_error);
       xhr.addEventListener('timeout',chat_error);
        xhr.send(fromData);
        request_chat_valid=false
    },1000)
}
// function button send_message

// function sond
function func_sond(e){
    elem=e.currentTarget;
    elem.classList.toggle("sond_off")
    elem.classList.toggle("sond_on")
    if(elem.classList.contains("sond_on")){
        speech_robot=true
    }
    else{
        speech_robot=false
    }
}

// function sond


//  Event menu

menu.addEventListener("click",main_menu_on_off)
// document.body.addEventListener('click',main_menu_blur)
// function main_menu_blur(e){
//     var source=e.target,
//     elem=menu.firstElementChild,
//     main_menu_etat=getComputedStyle(main_menu).display;
//     if((source!=elem)&&(source!=main_menu)&&(main_menu_etat!="none")){
//         main_menu.className="main_menu main_menu_anim_on"
//         elem.classList.toggle("fa-bars")
//         elem.classList.toggle("fa-xmark")
//             main_menu.classList.toggle("main_menu_anim_off")
//             main_menu.classList.toggle("main_menu_anim_on")
//             setTimeout(()=>{
//                 main_menu.style.display="none";
//             },2001)  
//     }
//     // alert(e.target)
// }

//  Event menu
// event button send_message
send_message.addEventListener("click",request_chat)
send_message.addEventListener("click",send_user)
send_message.addEventListener("click",firt_message_robot)
// event button send_message


// event sond
for(i=0,l=sond.length;i<l;i++){
    sond[i].addEventListener("click",func_sond);
}
// event sond


