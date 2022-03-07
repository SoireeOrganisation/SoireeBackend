function getCookie(name)
{
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
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
    for (i = startIndex; i <= endIndex; i++)
    {
        dataTable.deleteRow(i);
    }
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
let startPage = 1;
let startPageSize = 5;

if (!getCookie("key"))
{
    window.location.replace(`login`);
}
else
{
    getReviews(startPage, startPageSize);
}

