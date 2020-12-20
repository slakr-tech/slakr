const googleSignInBtn = document.getElementById('googleSignInBtn');
const googleSignUpBtn = document.getElementById('googleSignUpBtn');
const emailInputLogIn = document.getElementById('emailInputLogIn');
const emailInputCreateAccount = document.getElementById('emailInputCreateAccount');
const whenCreateAccount = document.getElementById('whenCreateAccount');
const signOutBtn = document.getElementById('signOutBtn');
const passwordInputLogIn = document.getElementById('passwordInputLogIn');
const passwordInputCreateAccount = document.getElementById('passwordInputCreateAccount');
const passwordInputCreateAccountConfirm = document.getElementById('passwordInputCreateAccountConfirm');

const userDetails = document.getElementById('userDetails');

console.log(firebase);

const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();

googleSignInBtn.onclick = () => auth.signInWithPopup(provider);
googleSignUpBtn.onclick = () => auth.signInWithPopup(provider);

signOutBtn.onclick = () => auth.signOut();

function authStateChange(user) {
    if (user) {
        // signed in
        whenSignedIn.hidden = false;
        whenSignedOut.hidden = true;
        whenCreateAccount.hidden = true;
        userDetails.innerHTML = `<h3>Hello ${user.displayName}!</h3> <p>User ID: ${user.uid}</p>`;
    } else {
        // not signed in
        whenSignedIn.hidden = true;
        whenSignedOut.hidden = false;
        whenCreateAccount.hidden = true;
        userDetails.innerHTML = '';
    }
}

function authErr(err) {
    let errorCode = err.code;
    let errorMessage = err.message;
    alert(errorMessage);
}

function showSignUp() {
    whenSignedIn.hidden = true;
    whenSignedOut.hidden = true;
    whenCreateAccount.hidden = false;
}

function signUp() {
    if (passwordInputCreateAccount.value == passwordInputCreateAccountConfirm.value) {
        auth.createUserWithEmailAndPassword(emailInputCreateAccount.value, passwordInputCreateAccount.value)
            .then(authStateChange)
            .catch(authErr);
    } else {
        alert('password and password confirm do not match')
    }
}

function signIn() {
    firebase.auth().signInWithEmailAndPassword(emailInputLogIn.value, passwordInputLogIn.value)
        .then(authStateChange)
        .catch(authErr);
}



auth.onAuthStateChanged(authStateChange);