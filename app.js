var express = require('express')
  , passport = require('passport')
  , TumblrStrategy = require('passport-tumblr').Strategy
  , SoundCloudStrategy = require('passport-soundcloud').Strategy;

var app = express();
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);

var TUMBLR_CLIENT_ID = '';
var TUMBLR_CLIENT_SECRET = '';
var SOUNDCLOUD_CLIENT_ID = '';
var SOUNDCLOUD_CLIENT_SECRET = '';

var receivedToken;
var receivedSecret;
var soundcloud_received_token; 
var soundcloud_received_secret;

app.configure(function() { 
  app.use(express.static(__dirname + '/public'));
  app.use(express.logger()); 
  app.use(express.cookieParser());
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(express.session({ secret: 'keyboard cat' }));
  app.use(passport.initialize());
  app.use(passport.session());
  app.use(app.router);
});
passport.serializeUser(function(user, done) {
  done(null, user);
});

passport.deserializeUser(function(obj, done) {
  done(null, obj);
});

passport.use(new TumblrStrategy({
    consumerKey: TUMBLR_CLIENT_ID,
    consumerSecret: TUMBLR_CLIENT_SECRET,
    callbackURL: ""
  },
  function(token, tokenSecret, profile, done) {
      receivedToken = token;
      receivedSecret = tokenSecret;
      return done(null, profile);
    }));

passport.use(new SoundCloudStrategy({
    clientID: SOUNDCLOUD_CLIENT_ID,
    clientSecret: SOUNDCLOUD_CLIENT_SECRET,
    callbackURL: ""
  },
  function(accessToken, refreshToken, profile, done) {
      soundcloud_received_token = accessToken;
      soundcloud_received_secret = refreshToken;
      return done(null, profile);
    }));
app.get('/', function (req, res)
{
    res.render('index.html');
});

app.get('/auth/tumblr',
  passport.authenticate('tumblr'));

app.get('/auth/tumblr/callback',
  passport.authenticate('tumblr', {
  failureRedirect: '/login',
  successRedirect: '/' })
  );

app.get('/auth/soundcloud',
  passport.authenticate('soundcloud'));

app.get('/auth/soundcloud/callback',
  passport.authenticate('soundcloud', { failureRedirect: '/login' }),
  function(req, res) {
    res.redirect('/');
  });

app.post('/create', function(req, res){
  var sys = require('sys'),
    exec = require('child_process').exec,
    child;
  console.log(soundcloud_received_token + 'here it is');
  console.log(receivedToken + ' and this');
  child = exec('python createPlaylist.py' + ' ' +
             TUMBLR_CLIENT_ID + ' ' +
             TUMBLR_CLIENT_SECRET + ' ' +
             receivedToken + ' ' +
             receivedSecret + ' ' +
 SOUNDCLOUD_CLIENT_ID + ' ' +
             SOUNDCLOUD_CLIENT_SECRET + ' ' +
             soundcloud_received_token + ' ' +
             soundcloud_received_secret ,
  function (error, stdout, stderr) {
    sys.print('stdout: ' + stdout);
    sys.print('stderr: ' + stderr);
    if (error !== null) {
      console.log('exec error: ' + error);
}})
setTimeout(function(){res.redirect('https://soundcloud.com/you/sets')},3000);
});

app.listen(process.env.PORT || 5000);