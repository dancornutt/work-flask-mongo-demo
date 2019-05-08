function myFunction() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("mylist");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function Filter(type) {
    var input, filter, table, tr, td, i, column;
    input = document.getElementById("select_" + type);
    filter = input.value;
    table = document.getElementById("AllTable");
    tr = table.getElementsByTagName("tr");
    if (type === "part_type") {
        column = 3;
    } else if (type === "clg_type") {
        column = 7;
    } else if (type === "side") {
        column = 8;
    } else if (type === "location") {
        column = 9;
    }
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[column];
        if (td) {
            if (td.innerHTML.indexOf(filter) > -1 && tr[i].style.display != "none") {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}
