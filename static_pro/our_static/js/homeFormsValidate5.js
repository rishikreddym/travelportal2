function scheduleFormValidate(){
           
  var x=document.forms['scheduleForm']['schedule-source'].value;
  var y=document.forms['scheduleForm']['schedule-dest'].value;  
           
  if(x=='u'){
    alert("Please select a source");return false;}
    if(y=='u'){
      alert("Please select a dest");return false;}
    if(x==y){
        alert("Source and Destination can't be same");return false;}
    return true;
}
function bookingFormValidate(){
            var x=document.forms['bookingForm']['booking-source'].value;
            var y=document.forms['bookingForm']['booking-dest'].value;  
           
            if(x=='u'){
              alert("Please select a source");return false;}
            if(y=='u'){
              alert("Please select a dest");return false;}
            if(x==y){
              alert("Source and Destination can't be same");return false;}
            return true;
          }
function preBookFormValidate(){
           
  var x=document.forms['preBookForm']['preBook-source'].value;
  var y=document.forms['preBookForm']['preBook-dest'].value;  
           
  if(x=='u'){
    alert("Please select a source");return false;}
    if(y=='u'){
      alert("Please select a dest");return false;}
    if(x==y){
        alert("Source and Destination can't be same");return false;}
    return true;
}
function bookFormValidate() {
  document.forms["bookForm"]["seats"].value = document.forms["preBookForm"]["preBook-seats"].value;
  document.forms["bookForm"]["date_time"].value = document.forms["preBookForm"]["preBook-date_time"].value;
  var flag=0;

  
  var chx = document.getElementsByTagName('input');
  for (var i=0; i<chx.length; i++) {
  	if (chx[i].type == 'radio' && chx[i].name=='select'){
  		flag ++;
  	}
    if (chx[i].type == 'radio' && chx[i].name=='select'  && chx[i].checked) {
      if(chx[i].value.charAt(0) == 'n'){
        var x =document.forms["preBookForm"]["preBook-source"].value;
        var y = document.forms["preBookForm"]["preBook-dest"].value;

        if(x==y){
          alert("Source and Destination must be different");
          return false;
        }

        if(x=='u' || y=='u'){
          alert("Please choose the source/destination from the given dropdown");
          return false;
        }

        document.forms["bookForm"]["source"].value = document.forms["preBookForm"]["preBook-source"].value;
        document.forms["bookForm"]["dest"].value = document.forms["preBookForm"]["preBook-dest"].value;

        var places = new Array();
        places["M"]="Mandi"
        places["K"]="Kamand"

        var prompt = confirm("Confirm your booking for :\nDateTime = " + document.forms["bookForm"]["date_time"].value + "\nFrom = "+ places[document.forms["bookForm"]["source"].value] + "\nTo = "+ places[document.forms["bookForm"]["dest"].value] + "\nSeats = "+document.forms["bookForm"]["seats"].value);

      }else{
        res = chx[i].value.split("|")
        var prompt = confirm("Confirm your seat in the booking with id = "+res[1]);
      }
    
      if(prompt==true)
        return true;
      else
        return false;
    } 
  }
  if(flag>0){
    alert("Please select an option from the available options.");
  }else{
   alert("Sorry, You can't book a vehicle at this time.");
 }
 return false;
}
