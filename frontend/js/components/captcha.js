export function captcha() {
    const load_new_captcha_image = document.getElementById("load-new-img");

    // ? Disabled for now - Must be use if we had 'Data confidentiality policy'
    // const id_data_confidentiality_policy = document.getElementById(
    //     "id_data_confidentiality_policy"
    // );
    // const btn_send_contact_form = document.getElementById("send-contact-form");

    if (load_new_captcha_image) {
        load_new_captcha_image.addEventListener("click", async function (ev) {
            ev.preventDefault();

            let reqHeader = new Headers();
            reqHeader.append("x-requested-with", "XMLHttpRequest");

            let initObject = {
                method: "GET",
                headers: reqHeader,
            };

            const response = await fetch(
                `${window.location.origin}/code-check/refresh/`,
                initObject
            );
            const new_img = await response.json();

            document.getElementById("id_captcha_0").value = new_img.key;
            document.getElementsByClassName("captcha")[0].src =
                new_img.image_url;
        });
    }

    // ? Disabled for now - Must be use if we had 'Data confidentiality policy'
    // if (id_data_confidentiality_policy) {
    //     if (id_data_confidentiality_policy.checked) {
    //         btn_send_contact_form.disabled = false;
    //     }

    //     id_data_confidentiality_policy.addEventListener(
    //         "change",
    //         function (ev) {
    //             if (ev.target.checked) {
    //                 btn_send_contact_form.disabled = false;
    //             } else {
    //                 btn_send_contact_form.disabled = true;
    //             }
    //         }
    //     );
    // }
}
