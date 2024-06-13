const searchInput = document.getElementById('searchinput');
const paginationDiv = document.querySelector('.pagination-div');
const resultsOutput = document.querySelector('.search-output');
const expendituresTable = document.querySelector('.expenditures-table');
const searchTable = document.querySelector('.search-table');

searchInput.addEventListener('keyup', (e) => {
    const searchval = e.target.value;
    if (searchval.trim().length > 0) {
        searchTable.innerHTML = ''; 
        
        // Make API call
        fetch('search-income/', {
            body: JSON.stringify({
                'searchText': searchval,
            }),
            method: "POST",
        }).then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                expendituresTable.style.display = 'none';
                paginationDiv.style.display = 'none';
                resultsOutput.style.display = 'block';

                if (data.length === 0) {
                    resultsOutput.innerHTML = 'No data found';
                } else {
                    resultsOutput.innerHTML = `<table class="table table-striped table-hover">
                        <thead class="thead-dark">
                            <tr>
                                <th scope="col">Amount</th>
                                <th scope="col">Category</th>
                                <th scope="col">Description</th>
                                <th scope="col">Date</th>
                            </tr>
                        </thead>
                        <tbody class="search-table">
                            ${data.map(item => `
                                <tr>
                                    <td>${item.amount}</td>
                                    <td>${item.source}</td>
                                    <td>${item.description}</td>
                                    <td>${item.date}</td>
                                     <td>
                                        <a href="${item.edit_url}" class="btn btn-secondary btn-sm">Edit</a>
                                        <a href="${item.delete_url}" class="btn btn-danger btn-sm">Delete</a>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>`;
                }
            });
    } else {
        expendituresTable.style.display = 'block';
        paginationDiv.style.display = 'block';
        resultsOutput.style.display = 'none';
        resultsOutput.innerHTML = '';
    }
});