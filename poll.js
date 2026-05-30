let votes = [0,0,0,0,0,0,0,0,0,0,0,0];

function castVote(index){

    if(loggedIn != "True"){
        alert("Please login to vote!");
        window.location.href = "/login";
        return;
    }
    votes[index]++;

    let hostelVotes = votes.slice(0,6);
    let totalHostel = hostelVotes.reduce((a,b)=>a+b,0);

    let academicVotes = votes.slice(6,12);
    let totalAcademic = academicVotes.reduce((a,b)=>a+b,0);

    document.getElementById("total").innerText = totalHostel;
    document.getElementById("total2").innerText = totalAcademic;

    for(let i=0;i<6;i++){
        let percent = totalHostel ? ((votes[i]/totalHostel)*100).toFixed(2) : 0;
        document.getElementById("p"+i).innerText = percent + "%";
    }

    for(let i=6;i<12;i++){
        let percent = totalAcademic ? ((votes[i]/totalAcademic)*100).toFixed(2) : 0;
        document.getElementById("p"+i).innerText = percent + "%";
    }
}