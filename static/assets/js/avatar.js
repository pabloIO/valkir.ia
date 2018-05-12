randomizarAvatar();
function randomizarAvatar() {
  // alert('Hola');
  document.getElementById('holder').innerHTML = "";
  // document.getElementById('holder2').innerHTML = "";
  // Se instancia una URI valida para contener la randomizacion de colores
  
  // HTML - Use http://www.w3.org/1999/xhtml
  // SVG - Use http://www.w3.org/2000/svg
  // XBL - Use http://www.mozilla.org/xbl
  // XUL - Use http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul

  var svgns = "http://www.w3.org/2000/svg";
  // console.log(svgns);

  var box = document.createElementNS(svgns, 'svg');

  var rows = 3;
  var columns = 3;
  var block_size = 50;
  // how i define the box size is a bit guess work for now
  var box_size = parseInt(rows -1) * parseInt(block_size);
  
  box.setAttribute('xmlns:xlink','http://www.w3.org/1999/xlink');
  box.setAttribute('width', box_size);
  box.setAttribute('height', box_size);
  box.setAttribute('viewbox', '0 0 100 100');
  box.setAttribute('class', 'box');
  
  var g = document.createElementNS(svgns, 'g');
  g.setAttribute('transform', 'translate(' + -((rows * block_size - box_size) / 2) + ' ' + -((rows * block_size - box_size) /2) + ') rotate(0 ' + (block_size * rows /2) + ' ' + (block_size * rows / 2) + ')');

  for (var i = 0; i < columns; i++) {
    //noprotect
    for (var j = 0; j < rows; j++) {
      var rect = document.createElementNS(svgns, 'rect');
      rect.setAttribute('width', block_size);
      rect.setAttribute('height', block_size);
      rect.setAttribute('fill', "rgba(" + getRandomRange(0, 255) + "," +  getRandomRange(0, 255) + "," + getRandomRange(0, 255) + ",1)");
      rect.setAttribute('x', i * block_size);
      rect.setAttribute('y', j * block_size);
      
      g.appendChild(rect);
    }
  }
  box.appendChild(g);
  document.getElementById('holder').appendChild(box);
  document.getElementById('holder2').appendChild(box);
  
  function getRandomRange(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
  }
}

