
class courseDetails {
    constructor(course, rootElm) {
        this.course = course
        this.rootElm= rootElm;
        this.isRendered = false;
    }
    destructor(){
        this.course = null;
        this.rootElm = null;
    }
    renderHtml(){
        this.rootElm.innerHTML = `<div class="rounded p-2 table-responsive"> 
                    <table class="table table-bordered">
                        <tr>
                        <td><span>Name</span><br><b>${ this.course.name }</b></td>
                        <td><span>Code</span><br><b>${ this.course.code }</b></td>
                        <td><span>Level</span><br><b>${ this.course.level }</b></td>
                        <td><span>Semester</span><br><b>${ this.course.semester }</b></td>
                        </tr><tr>
                        <td><span>Credit Hours</span><br><b>${ this.course.creditHours }</b></td>
                        <td><span>Academic Year</span><br><b>${ this.course.academicYear }</b></td>
                        <td><span>Programme</span><br><b>${ this.course.programme }</b></td>
                        <td><span>Lecturer</span><br><i class="fa fa-user-circle me-2"></i><b>${ this.course.lecturer }</b></td>
                        </tr>
                        
                        <tr>
                        <td colspan="4"><span>${this.course.description ? 'Description': "Description".strike() }</span></td>
                        </tr>
                    </table>
                    <div class="my-3">${this.course.description }</div>
                </div>`;
        this.isRendered = true
    }
}

class Assignments {
    constructor(assessment, htmlElement) {
        this.assessment = assessment;
        this.parentElment = htmlElement
    }

    renderHtml(){
        this.parentElment.innerHTML = `
<h2 class="text-center display-6">Assessment</h2>
<div class="d-flex flex-wrap justify-content-center gap-3 bg-light-blue rounded p-2 shadow-sm mb-3">
<div class="card">
<div class="card-body"><h5>Prepared Assessment</h5><a href="" class="stretched-link">New</a></div>
</div><div class="card">
<div class="card-body"><h5>Manage All Assessment</h5><a href="" class="stretched-link">Manage</a></div>
</div><div class="card">
<div class="card-body"><h5>Record Assessment</h5><a href="" class="stretched-link">Manuel</a></div>
</div>
<div class="card">
<div class="card-body"><h5>Academic Calender</h5><a href="" class="stretched-link">Schedule Task</a></div>
</div><div class="card">
<div class="card-body"><h5>Assessment Constraints</h5><a href="" class="stretched-link">Config</a></div>
</div>
</div>
<div class="d-flex flex-wrap gap-3">
    <div class="card h-100">
         <ul class="list-group list-group-flush">
            <li class="list-group-item"><span>This week</span><br><b>3 Assignment</b><a href="" class="ms-2">view</a></li>
            <li class="list-group-item"><span>This Month</span><br><b>7 Assignment</b><a href="" class="ms-2">view</a></li>
            <li class="list-group-item"><span>This Semester</span><br><b>21 Assignment</b><a href="" class="ms-2">view</a></li>
        </ul>
    </div>
    <div class="card h-100">
        <div class="card-body">
            <span>This Month</span><br><b>12 Assessments</b>
        </div>
    </div>
    <div class="card h-100">
        <div class="card-body">
            <span>This Semester</span><br>
            <b>20 Assessment</b>
        </div>
    </div>
</div>
<div class="alert alert-primary my-3"> WE ARE WORKING ON A REAL-TIME GRAPH OF ASSESSMENT STATISTICS</div>`
    }
}


class Students{
    constructor(htmlElement) {
        this.rootELm = htmlElement
    }

    renderHtml() {
        this.rootELm.innerHTML = `<div>
<div class="d-flex flex-wrap gap-3 mb-3">
    <div class="card">
        <div class="card-body">
            <h5>Record Assessment</h5>
        </div>
        <div class="card-footer">
            <a href="#" class="btn btn-info btn-sm">Record</a>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <h5>Conduct Assessment</h5>
        </div>
        <div class="card-footer">
            <a href="#" class="btn btn-info btn-sm">Conduct</a>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <h5>View Assessment</h5>
        </div>
        <div class="card-footer">
            <a href="#" class="btn btn-info btn-sm">View</a>
        </div>
    </div>
</div>

<div class="card-group">
    <div class="card hover_shadow">
        <div class="card-header"><span class="float-start" title="Department Name">Programme Name</span><small class="float-end text-muted">Level 100</small></div>
            <div class="list-group list-group-flush">
                <p class="list-group-item"><span>Student Total</span><br>
            <b>1212 Students</b></p>
                <p class="list-group-item"><span>Active Student (Online)</span><br>
            <b>1200 Students</b></p>
                <p class="list-group-item"><span>Student Offline </span><br>
            <b>12 Students</b>  </p>
        </div>
    </div>
    <div class="card hover_shadow">
        <div class="card-header"><span class="float-start" title="Department Name">Programme Name</span><small class="float-end text-muted">Level 200</small></div>
            <div class="list-group list-group-flush">
                <p class="list-group-item"><span>Student Total</span><br>
            <b>1212 Students</b></p>
                <p class="list-group-item"><span>Active Student (Online)</span><br>
            <b>1200 Students</b></p>
                <p class="list-group-item"><span>Student Offline </span><br>
            <b>12 Students</b>  </p>
        </div>
    </div>
    <div class="card hover_shadow">
        <div class="card-header"><span class="float-start" title="Department Name">Programme Name</span><small class="float-end text-muted">Level 300</small></div>
            <div class="list-group list-group-flush">
                <p class="list-group-item"><span>Student Total</span><br>
            <b>1212 Students</b></p>
                <p class="list-group-item"><span>Active Student (Online)</span><br>
            <b>1200 Students</b></p>
                <p class="list-group-item"><span>Student Offline </span><br>
            <b>12 Students</b>  </p>
        </div>
    </div>
    
</div>
</div>`
    }
}