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
            addRowToDataTable(data["reviewer"]["name"],
              data["subject"]["name"],
              data["category"]["name"],
              data["score"],
              data["note"]);
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

