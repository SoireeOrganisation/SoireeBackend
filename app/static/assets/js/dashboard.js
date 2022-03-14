async function validateFormAndSend()
{
    var form = document.getElementById("bonusForm");

    if (form.checkValidity())
    {
        $('#bonusModal').modal('hide');
        await new Promise(r => setTimeout(r, 300));
        setBonus();
        if (form.classList.contains("was-validated"))
        {
            form.classList.remove("was-validated");
        }
        return;
    }

     form.classList.add("was-validated");
}

$(document).on('submit', '[data-validator]', function () {
    new Validator($(this));
});



function getCookie(name)
{
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function resetStaffSelect()
{
    document.getElementById('bonusName').value = '';
    $('#staffSelect option').prop('selected', false);
}

function setBonus()
{
    $.ajax({url: "/api/bonuses",
            type: "POST",
            cache: false,
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
            data:
                JSON.stringify({
                    key: getCookie("key"),
                    name: document.getElementById("bonusName").value,
                    userId: document.getElementById("staffSelect").value
                }),
                success: () => {}
            });
    resetStaffSelect();
}

function updateDataTable(result)
{
    if (result)
    {
        var dataTable = document.getElementById("dataTable");
        clearDataTableRows(2, dataTable.rows.length - 1);
        for (i = 0; i < result.length; i++)
        {
            let data = result[i];
            addRowToDataTable(data["reviewer"]["name"] + data["reviewer"]["surname"] + data["reviewer"]["patronymic"],
              data["subject"]["name"],
              data["category"]["name"] + data["category"]["surname"] + data["category"]["patronymic"],
              data["score"],
              data["note"] || "-");
        }
    }
}

function clearDataTableRows(startIndex, endIndex)
{
    var dataTable = document.getElementById("dataTable");
    while(dataTable.rows.length > 2) {
      dataTable.deleteRow(1);
    }
}

function updateReviews()
{
    let startPage = 1;
    let startPageSize = document.getElementById("dataTableSelect").value;
    let el = document.getElementById("endIndex");
    el.innerText = startPageSize;
    getReviews(startPage, startPageSize);
}

function getReviews(page, pageSize)
{
    $.ajax({url: "/api/reviews",
            type: "GET",
            cache: true,
            data:
                {
                    key: getCookie("key"),
                    page: page,
                    pageSize: pageSize
                },
                success: updateDataTable
            });
}

function addRowToDataTable(reviewerName, subjectName, categoryName, score, note)
{
    var dataTable = document.getElementById("dataTable");
    row = dataTable.insertRow(dataTable.rows.length - 1);
    reviewerNameCell = row.insertCell(0);
    reviewerNameCell.innerText = reviewerName;
    subjectNameCell = row.insertCell(1);
    subjectNameCell.innerText = subjectName;
    categoryNameCell = row.insertCell(2);
    categoryNameCell.innerText = categoryName;
    scoreCell = row.insertCell(3);
    scoreCell.innerText = score;
    noteCell = row.insertCell(4);
    noteCell.innerText = note;
}

const host = window.location.host;


if (!getCookie("key"))
{
    window.location.replace(`login`);
}

document.addEventListener("DOMContentLoaded", function() {
  updateReviews();
});

var gl;
function d()
{
    var dataTable = document.getElementById("dataTable");
gl = TableExport(dataTable, {
  headers: true,                      // (Boolean), display table headers (th or td elements) in the <thead>, (default: true)
  footers: true,                      // (Boolean), display table footers (th or td elements) in the <tfoot>, (default: false)
  formats: ["xlsx", "csv"],    // (String[]), filetype(s) for the export, (default: ['xlsx', 'csv', 'txt'])
  filename: "report",                     // (id, String), filename for the downloaded file, (default: 'id')
  bootstrap: true,                   // (Boolean), style buttons using bootstrap, (default: true)
  exportButtons: true,                // (Boolean), automatically generate the built-in export buttons for each of the specified formats (default: true)
  position: "bottom",                 // (top, bottom), position of the caption element relative to table, (default: 'bottom')
  ignoreRows: null,                   // (Number, Number[]), row indices to exclude from the exported file(s) (default: null)
  ignoreCols: null,                   // (Number, Number[]), column indices to exclude from the exported file(s) (default: null)
  trimWhitespace: true,               // (Boolean), remove all leading/trailing newlines, spaces, and tabs from cell text in the exported file(s) (default: false)
  RTL: false,                         // (Boolean), set direction of the worksheet to right-to-left (default: false)
  sheetname: "Отзывы на сотрудников"                     // (id, String), sheet name for the exported spreadsheet, (default: 'id')
});
var c = document.getElementsByClassName("tableexport-caption")[0];
dataTable.removeChild(c);
document.getElementById("dataTable-1").appendChild(c);
document.getElementsByClassName("xlsx")[0].style = "margin-right: 1%;"
document.getElementsByClassName("xlsx")[0].classList.remove("btn-default")
document.getElementsByClassName("xlsx")[0].classList.add("btn-outline-dark")
document.getElementsByClassName("csv")[0].classList.remove("btn-default")
document.getElementsByClassName("csv")[0].classList.add("btn-outline-dark")
}

