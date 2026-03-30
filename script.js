async function loadStudents() {
    // 1. Request data from FastAPI
    const response = await fetch('http://127.0.0.1:8000/students');
    const students = await response.json();

    // 2. Display it in HTML
    const list = document.getElementById('student-list');
    list.innerHTML = ""; 
    students.forEach(s => {
        const li = document.createElement('li');
        li.textContent = `${s.email} - Semester ${s.semester}`;
        list.appendChild(li);
    });
}

// Run when page loads
load_students();