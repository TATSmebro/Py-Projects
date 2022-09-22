import reactors as R
import image as I

### TYPES ###

data PlatformLevel:
  | top
  | middle
  | bottom
end

data GameStatus:
  | ongoing
  | transitioning(ticks-left :: Number)
  | game-over
end

type Platform = {
  x :: Number,
  y :: Number,
  dx :: Number,
}

type Egg = {
  x :: Number,
  y :: Number,
  dx :: Number,
  dy :: Number,
  ay :: Number,
  is-airborne :: Boolean,
}

type State = {
  game-status :: GameStatus,
  egg :: Egg,
  top-platform :: Platform,
  middle-platform :: Platform,
  bottom-platform :: Platform,
  current-platform :: PlatformLevel,
  other-platforms :: List<Platform>,
  score :: Number,
  lives :: Number,
}

### ADDITIONAL FUNCITONS ###

fun num-generator(x :: Number) -> Number:
  num = num-random(x) + num-random(-1 * x)
  if num == 0:
    num + 1
  else:
    num
  end
end

### CONSTANTS ###

FPS = 60

SCREEN-WIDTH = 300
SCREEN-HEIGHT = 500

TOP-PLATFORM-Y = SCREEN-HEIGHT / 4
MID-PLATFORM-Y = SCREEN-HEIGHT / 2
BOT-PLATFORM-Y = TOP-PLATFORM-Y * 3
PLATFORM-WIDTH = 50
PLATFORM-HEIGHT = 10
PLATFORM-COLOR = 'brown'
PLATFORM-SPEED = 5
INITIAL-BOTTOM-PLATFORM-SPEED = num-generator(PLATFORM-SPEED)

EGG-RADIUS = 12
EGG-JUMP-HEIGHT = -14
EGG-COLOR = 'bisque'

GRAVITY = 0.5
TRANSITION-DY = 250 / (2 * FPS)

INITIAL-STATE ={
  game-status : ongoing,
  egg : {x: (SCREEN-WIDTH / 2) + (PLATFORM-WIDTH / 2), y: BOT-PLATFORM-Y - EGG-RADIUS, dx: INITIAL-BOTTOM-PLATFORM-SPEED, dy: 0, ay: 0, is-airborne: false},
  top-platform : {x: SCREEN-WIDTH / 2, y: TOP-PLATFORM-Y, dx: num-generator(PLATFORM-SPEED)},
  middle-platform : {x: SCREEN-WIDTH / 2, y: MID-PLATFORM-Y, dx: num-generator(PLATFORM-SPEED)},
  bottom-platform : {x: SCREEN-WIDTH / 2, y: BOT-PLATFORM-Y, dx: INITIAL-BOTTOM-PLATFORM-SPEED},
  current-platform : bottom,
  other-platforms : [list:],
  score : 0,
  lives : 12,
}

### DRAWING ###

fun draw-egg(state :: State, img :: Image) -> Image:
  egg = circle(EGG-RADIUS, 'solid', EGG-COLOR)
  place-image(egg, state.egg.x, state.egg.y, img)
end

fun draw-platform(state :: State, img :: Image) -> Image:
  platform-img = rectangle(PLATFORM-WIDTH, PLATFORM-HEIGHT, 'solid', PLATFORM-COLOR)

  cases (List) state.other-platforms:
    |empty =>
      img
        ^ place-image-align(platform-img, state.top-platform.x, state.top-platform.y, 'left', 'top', _)
        ^ place-image-align(platform-img, state.middle-platform.x, state.middle-platform.y, 'left', 'top', _)
        ^ place-image-align(platform-img, state.bottom-platform.x, state.bottom-platform.y, 'left', 'top', _)
    |link(first, rest) => 
      img
        ^ place-image-align(platform-img, state.other-platforms.get(0).x, state.other-platforms.get(0).y, 'left', 'top', _)
        ^ place-image-align(platform-img, state.other-platforms.get(1).x, state.other-platforms.get(1).y, 'left', 'top', _)
        ^ place-image-align(platform-img, state.top-platform.x, state.top-platform.y, 'left', 'top', _)
        ^ place-image-align(platform-img, state.middle-platform.x, state.middle-platform.y, 'left', 'top', _)
        ^ place-image-align(platform-img, state.bottom-platform.x, state.bottom-platform.y, 'left', 'top', _)
  end
end

fun draw-score(state :: State, img :: Image) -> Image:
  text-img = text(num-to-string(state.score), 24, "black")
  I.place-image(text-img, SCREEN-WIDTH / 2, SCREEN-HEIGHT / 10, img)
end

fun draw-lives(state :: State, img :: Image) -> Image:
  text-img = text('Lives: ' + num-to-string(state.lives), 20, "black")
  I.place-image(text-img, SCREEN-WIDTH - 50, SCREEN-HEIGHT / 25, img)
end

fun draw-game-over(state :: State, img :: Image) -> Image:
  cases (GameStatus) state.game-status:
    | ongoing => img
    | transitioning(_) => img
    | game-over =>
      text-img = text("GAME OVER", 48, "red")
      I.place-image(text-img, SCREEN-WIDTH / 2, SCREEN-HEIGHT / 2, img)
  end
end

fun draw-handler(state :: State) -> Image:
  canvas = empty-color-scene(SCREEN-WIDTH, SCREEN-HEIGHT, "light-blue")

  canvas
    ^ draw-egg(state, _)
    ^ draw-platform(state, _)
    ^ draw-score(state, _)
    ^ draw-lives(state, _)
    ^ draw-game-over(state, _)
end

### KEYBOARD ###

fun key-handler(state :: State, key :: String) -> State:
  if key == ' ':
    cases (GameStatus) state.game-status:
      | ongoing => 
        if state.egg.is-airborne:
          state
        else:
          state.{egg: state.egg.{dy: EGG-JUMP-HEIGHT, ay: GRAVITY, is-airborne: true}}
        end
      | transitioning(_) => state
      | game-over => INITIAL-STATE
    end
  else:
    state
  end
end

### TICKS ###

fun update-egg-velocity(state :: State) -> State:
  if state.egg.is-airborne:
    state.{egg: state.egg.{dx: 0, dy: state.egg.dy + state.egg.ay}}
  else:
    cases (PlatformLevel) state.current-platform:
      |top => state.{egg: state.egg.{dx: state.top-platform.dx, dy: 0}}
      |middle => state.{egg: state.egg.{dx: state.middle-platform.dx, dy: 0}}
      |bottom => state.{egg: state.egg.{dx: state.bottom-platform.dx, dy: 0}}
    end
  end
end

fun update-egg-coordinate(state :: State) -> State:
  state.{egg: state.egg.{x: state.egg.x + state.egg.dx, y: state.egg.y + state.egg.dy}}
end

fun update-platform-coordinate(state :: State) -> State:

  fun update-platform-velocity(platform :: Platform) -> Platform:
    if ((platform.x + PLATFORM-WIDTH) >= SCREEN-WIDTH) or (platform.x <= 0):
      platform.{dx: platform.dx * -1}
    else:
      platform
    end
  end

  top-platform = update-platform-velocity(state.top-platform)
  middle-platform = update-platform-velocity(state.middle-platform)
  bottom-platform = update-platform-velocity(state.bottom-platform)

  state.{
    top-platform: top-platform.{x: top-platform.x + top-platform.dx},
    middle-platform: middle-platform.{x: middle-platform.x + middle-platform.dx},
    bottom-platform: bottom-platform.{x: bottom-platform.x + bottom-platform.dx},
  }
end

fun update-collision(state :: State) -> State:
  fun update-collision-helper(target-platform :: Platform, plat-level :: PlatformLevel, prev-plat :: Platform) -> State:
    egg-bottom = state.egg.y + EGG-RADIUS

    center-within-platform = (target-platform.x <= state.egg.x) and (state.egg.x <= (target-platform.x + PLATFORM-WIDTH))
    bottom-in-collision = (egg-bottom >= target-platform.y) and (egg-bottom <= (target-platform.y + PLATFORM-HEIGHT))
    egg-is-falling = state.egg.dy >= 0
    egg-is-catched = (state.egg.is-airborne and egg-is-falling) and (center-within-platform and bottom-in-collision)

    egg-at-bottom-of-screen = (state.egg.y + EGG-RADIUS) >= SCREEN-HEIGHT

    if egg-is-catched:
      state.{egg: state.egg.{y: target-platform.y - EGG-RADIUS, is-airborne: false}, current-platform: plat-level, score: state.score + 1}
    else if egg-at-bottom-of-screen:
      state.{egg: state.egg.{x: prev-plat.x + (PLATFORM-WIDTH / 2), y: prev-plat.y - EGG-RADIUS, is-airborne: false}, lives: state.lives - 1}
    else:
      state
    end
  end

  if state.current-platform == bottom:
    update-collision-helper(state.middle-platform, middle, state.bottom-platform)
  else:
    update-collision-helper(state.top-platform, top, state.middle-platform)
  end

end

fun update-level(state :: State) -> State:
  fun generate-platforms() -> List<Platform>:
    future-top = {x: SCREEN-WIDTH / 2, y: -1 * TOP-PLATFORM-Y, dx: num-generator(PLATFORM-SPEED)} 
    future-mid = {x: SCREEN-WIDTH / 2, y: 0, dx: num-generator(PLATFORM-SPEED)}
    [list: future-mid, future-top]
  end

  if state.current-platform == top:
    state.{other-platforms: state.other-platforms.append(generate-platforms()), game-status: transitioning(2 * FPS)}
  else:
    state
  end
end

fun update-if-game-over(state :: State) -> State:
  if state.lives <= 0:
    state.{game-status: game-over}
  else:
    state
  end
end

fun transition-game(state :: State) -> State:
  egg = state.egg.{y: state.egg.y + TRANSITION-DY}
  top-platform = state.top-platform.{y: state.top-platform.y + TRANSITION-DY}
  middle-platform = state.middle-platform.{y: state.middle-platform.y + TRANSITION-DY}
  bottom-platform = state.bottom-platform.{y: state.bottom-platform.y + TRANSITION-DY}
  future-middle = state.other-platforms.get(0).{y: state.other-platforms.get(0).y + TRANSITION-DY}
  future-top = state.other-platforms.get(1).{y: state.other-platforms.get(1).y + TRANSITION-DY}
  
  state.{
    game-status: transitioning(state.game-status.ticks-left - 1), 
    egg: egg,
    top-platform : top-platform,
    middle-platform : middle-platform,
    bottom-platform : bottom-platform,
    other-platforms : [list: future-middle, future-top]
  }
end

fun tick-handler(state :: State) -> State:
  cases (GameStatus) state.game-status:
    | ongoing =>
      state
        ^ update-platform-coordinate(_)
        ^ update-egg-velocity(_)
        ^ update-egg-coordinate(_)
        ^ update-collision(_)
        ^ update-level(_)
        ^ update-if-game-over(_)
    | transitioning(ticks-left) => 
      if ticks-left > 0:
        transition-game(state)
      else:
        state.{game-status: ongoing, top-platform: state.other-platforms.get(1), middle-platform: state.other-platforms.get(0), bottom-platform: state.top-platform, current-platform: bottom, other-platforms: [list: ]}
      end
    | game-over => state
  end
end

### MAIN ###

world = reactor:
  title: 'CS 12 MP Egg Toss',
  init: INITIAL-STATE,
  to-draw: draw-handler,
  seconds-per-tick: 1 / FPS,
  on-tick: tick-handler,
  on-key: key-handler,
end


R.interact(world)