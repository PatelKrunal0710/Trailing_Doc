var fstatus = document.getElementById("fsdd")
fstatus.onchange = function(){
    var db = document.getElementById("fsdd").value
    if(db=="Suspend"){
        document.getElementById("filecomment").style.display = 'block'
        document.getElementById("filecomment1").style.display = 'block'
    }else{
        document.getElementById("filecomment").style.display = 'none'
        document.getElementById("filecomment1").style.display = 'none'
    }
    var Table = document.getElementById("table")
    for(var i=1; i<Table.rows.length; i++){
        var ab = document.getElementById("ddstatus_"+i)
        ab.value = db
    }
}

function mnd(){
    var Table = document.getElementById("table")
    for(var i=1; i<Table.rows.length; i++){
    var ddv = document.getElementById("ddstatus_"+i).value
    if(ddv=="Fail"){
        var cmt = document.getElementById("comment_"+i).required=true
    }else{
        var cmt = document.getElementById("comment_"+i).required=false
    }
}
}

function h(){
var Table = document.getElementById("table")
for(var i=1; i<Table.rows.length; i++){
    var h = document.getElementById("ddstatus_"+i).value  
    if (h =="Fail"){
        document.getElementById("ddstatus_"+i).style.backgroundColor='red'
    }else if(h=="Pass"){
        document.getElementById("ddstatus_"+i).style.backgroundColor="green"
    }else{
        document.getElementById("ddstatus_"+i).style.backgroundColor="white"
    }
    }    
}


