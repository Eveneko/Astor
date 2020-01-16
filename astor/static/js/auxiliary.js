var randomImage = ()=>{
    return "/static/images/avatar/p"+Math.floor((Math.random() * 100)) + ".png";
}

var getImageFromID = (id)=>{
    return "/static/images/avatar/p"+ id % 100 + ".png";
}