$(document).ready(function() {
    $( '.add-anothertecido' ).click(function(e) {
        e.preventDefault();
        showAddAnotherPopup( $( this ) );
    });
});

/* Credit: django.contrib.admin (BSD) */

function showAddAnotherPopup(triggeringLink) {
    /*

    Pause here with Firebug's script debugger.

    */
    var name = triggeringLink.attr( 'id' ).replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.attr( 'href' );

    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href += '&_popup=1';
    }

    href += '&winName=' + name;

    var win = window.open( href, name , 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();

    return false;
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);

    if (elem) {
        if (elem.nodeName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        }
    } else {
        console.log("Could not get input id for win " + name);
    }

    win.close();
}

function html_unescape(text) {
 // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/</g, '');
    text = text.replace(/"/g, '"');
    text = text.replace(/'/g, "'");
    text = text.replace(/&/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    text = text.replace(/\[/g, '__braceleft__');
    text = text.replace(/\]/g, '__braceright__');
    return text;
} 