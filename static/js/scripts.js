switch( window.location.pathname ){
    case "/panel/main":
        const statistics_a = document.getElementById("statistics-a");
        const statistics_li = document.getElementById("statistics-li");
        statistics_a.classList.add("active");
        statistics_li.classList.add("active");
        break;

    case "/panel/settings":
        const settings_a = document.getElementById("settings-a");
        const settings_li = document.getElementById("settings-li");
        settings_a.classList.add("active");
        settings_li.classList.add("active");
        break;
}