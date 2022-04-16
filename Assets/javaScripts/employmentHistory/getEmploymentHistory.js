
function getEmployHistoryAjaxCall(url, containerElm) {
    $.ajax({
        url: url,
        success: response => {
        const { hasHistory, companyName,address,state,city,specific_duty,jobTitle,supervisor,employedFrom, employedTo,whyLeave } = response;
        if (hasHistory || jobTitle){
            containerElm.innerHTML = `
            <div class="d-flex gap-3 my-1 p-2 align-items-center rounded bg-light-${ hasHistory ? 'green' : 'red' }" style="width: fit-content"><span>Has Employement History</span><span class="fa fa-toggle-${hasHistory===true? 'on' : 'off'} fa-2x"></span></div>
            <ul class="list-group">
           <li class="list-group-item">
                <small>Institution Name</small><br>
                <b>${ companyName}</b>
            </li>
             <li class="list-group-item">
                <small>Job Title</small><br>
                <b>${ jobTitle}</b>
            </li>
             <li class="list-group-item">
                <small>Specific Duty</small><br>
                <div>${ specific_duty }</div>
            </li>
             <li class="list-group-item">
                <small>Supervisor</small><br>
                <b>${ supervisor }</b>
            </li>
             <li class="list-group-item">
                <small>Company Address</small><br>
                <b>${ address }</b>
            </li>
             <li class="list-group-item">
                <small>State</small><br>
                <b>${ state }</b>
            </li>
             <li class="list-group-item">
                <small>City</small><br>
                <b>${ city }</b>
            </li>
             <li class="list-group-item">
                <small>Employed From</small><br>
                <b>${ employedFrom }</b><i> -to- </i>
                <b>${ employedTo }</b>
            </li>
             <li class="list-group-item">
                <small>Why Leave the Institution</small><br>
                <b>${ whyLeave !== null ? whyLeave : 'N\\A' }</b>
            </li>
            
        </ul>`
        }
        else{
            containerElm.innerHTML = `<div class="col-md-7 mx-auto"><div class="alert alert-warning d-flex justify-content-between align-items-center"><span>${response.description}</span> <span class="fa fa-exclamation-circle fa-spin"></span></div></div>`
            }
        },
        errors: response => {alert('Please try again, later!')}
    })

}


function loadMyInformationALecturer(url, containerElm) {
    $.ajax({
        url:url,
        success: response => {
           containerElm.innerHTML = `<div class="col-md-7 col-lg-5 mx-auto">
                <h6 class="text-center my-2">Application Form</h6>
                <ul class="list-group shadow ">
                   <li class="list-group-item">
                    <small>Identity</small><br><b>${ response.identity }</b>
                    </li>
                   <li class="list-group-item"><small>Identity</small><br><b>${ response.department }</b></li>
                   <li class="list-group-item "><small>Application Letter</small><br><b><a href="${ response.applicationLetter }">Application Letter</a></b></li>
                   <li class="list-group-item "><small>CV</small><br><a href="${response.cv }"><b>Curricullum Vitae</b></a></li>
                   <li class="list-group-item list-group-item-text list-group-item-${response.isActive ? 'success': 'danger' }"><small>Status</small><br>${ response.isActive.toString().toUpperCase().bold() }</li>
                </ul>
        </div>         
`
        },
        errors: ()=>alert('Please try again, later!')
    })
}

