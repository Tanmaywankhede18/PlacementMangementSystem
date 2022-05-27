// console.log("Script Loaded successfully!!")
// $('#add_event_form').submit(function(e){
//     // e.preventDefault()
//     event_from_data = new FormData(this)
//     var view_modal = document.getElementById("view_modal");
//     $.ajax({
//         url:'',
//         processData: false,
//         contentType:false,
//         type:'POST',
//         data:event_from_data,
//         succcess:function(res){
//             console.log(res)
//             view_modal.style.display = 'none'
//         }
//     })
    
//     if ( window.history.replaceState ) {
//         window.history.replaceState( null, null, window.location.href );
//       }
// })

// $('#update_profile').submit(function(e){
//     e.preventDefault()
//     profile_data = new FormData(this)
//     console.log("Here...............................")
//     $.ajax({
//         url:'',
//         type:'POST',
//         processData: false,
//         contentType:false,
//         data:profile_data,
//         succcess:function(res){
//             console.log(res)
//             view_modal.style.display = 'none'
//         }
//     })
// })