/**
 * Created by Jarred on 18/09/2017.
 */


function DisplayHideFilter(obj_id) {
    var obj = document.getElementById(obj_id)
    if (obj.style.display == 'block') {
        obj.style.display = 'none';
    }
    else {
        obj.style.display = 'block';
    }
}
