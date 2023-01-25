/*const container=document.querySelector('.seat-container');
const seats=document.querySelectorAll('.seat:not(.occupied');
const num=document.getElementById('num');
const price=document.getElementById('price');
const movieSelect=document.getElementById('movie');

let ticketPrice =+movieSelect.value;

//保存selected movie的index,和ticketPrice
function setMovieData(movieIndex, moviePrice){
    localStorage.setItem('selectedMovieIndex',movieIndex);
    localStorage.setItem('selectedMoviePrice',moviePrice);
}

//更新num
function updateSelectedCount(){
    const selectedSeats=document.querySelectorAll('.seat.selected');
    const seatsIndex=[...selectedSeats].map(seat=>[...seats].indexOf(seat));//返回一个新数组index
    
    localStorage.setItem('selectedSeats',JSON.stringify(seatsIndex));

    const selectedSeatsCount=selectedSeats.length;

    num.innerText=selectedSeatsCount;
    price.innerText=selectedSeatsCount*ticketPrice;

setMovieData(movieSelect.selectedIndex,movieSelect.value);
}

//从localStorage获取数据selectedSeats数据，并把被选中的seat加一个selected属性，更新和populate UI
function populateUI(){
    selectedSeats=JSON.parse(localStorage.getItem('selectedSeats'));//JSON.parse() 方法将数据转换为 JavaScript 对象。

    if(selectedSeats!=null&&selectedSeats.length>0){
        seats.forEach((seat,index)=>{
            if(selectedSeats.indexOf(index)>-1){
                seat.classList.add('selected');
            }
        });

    }
}

//选择movie事件
movieSelect.addEventListener('change',e=>{
    ticketPrice=+e.target.value;
    updateSelectedCount();
});

//点击seat事件
container.addEventListener('click', e => {
    if (
      e.target.classList.contains('seat') &&
      !e.target.classList.contains('occupied')
    ) {
      e.target.classList.toggle('selected');
  
      updateSelectedCount();
    }
  });*/
  var check_num1 = 0;
  var check_num2 = 0;
  function check1(){ 
   if(event.srcElement.checked==true)
    check_num1++;
   else 
    check_num1--;   
   if(check_num1>3)
   {
    alert("超過數量！");
    event.srcElement.checked=false;
    check_num1--;
   }  

  }
  function check2(){ 
    if(event.srcElement.checked==true)
     check_num2++;
    else 
     check_num2--;   
    if(check_num2>3)
    {
     alert("超過數量！");
     event.srcElement.checked=false;
     check_num2--;
    }  
 
   }