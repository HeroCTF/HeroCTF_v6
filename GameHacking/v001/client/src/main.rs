use std::{thread::sleep, time::Duration};

use character::{Character, CharacterActionState};
use client::{server_connect, server_send_game_start_time};
use macroquad::prelude::*;
use macroquad_particles::{self as particles, AtlasConfig, BlendMode, Emitter, EmitterConfig};

mod character;
mod character_select;
mod client;
mod enemy;
mod level_one;
mod menu;
mod questing;
mod misc;

use level_one::level_one_draw;
use macroquad_platformer::World;
use questing::QuestLog;

use crate::enemy::Enemy;

fn smoke() -> particles::EmitterConfig {
    particles::EmitterConfig {
        lifetime: 3.,
        lifetime_randomness: 0.5,
        amount: 200,
        size: 1.,
        initial_direction_spread: 1.6,
        atlas: Some(AtlasConfig::new(4, 4, 0..8)),
        ..Default::default()
    }
}


fn image_menu(background_texture: &Texture2D, flag : &str)
{
    let screen_width = screen_width();
    let screen_height = screen_height();

    let params = DrawTextureParams {
        dest_size: Some(vec2(screen_width, screen_height)),
        source: None,
        rotation: 0.,
        flip_x: false,
        flip_y: false,
        pivot: None,
    };

    draw_texture_ex(
        background_texture,
        0.0,
        0.0,
        Color::from_rgba(255, 255, 255, 255),
        params,
    );

    draw_text(
        "Giam v0.01",
        20.0,
        20.0,
        30.0,
        Color::from_rgba(255, 255, 255, 255),
    );

    draw_text(
        &flag,
        20.0,
        50.0,
        20.0,
        Color::from_rgba(255, 255, 255, 255),
    );
}

fn main_menu(background_texture: &Texture2D, input: &mut String) {
    let screen_width = screen_width();
    let screen_height = screen_height();

    let params = DrawTextureParams {
        dest_size: Some(vec2(screen_width, screen_height)),
        source: None,
        rotation: 0.,
        flip_x: false,
        flip_y: false,
        pivot: None,
    };

    draw_texture_ex(
        background_texture,
        0.0,
        0.0,
        Color::from_rgba(255, 255, 255, 255),
        params,
    );

    draw_text(
        "Giam v0.01",
        20.0,
        20.0,
        30.0,
        Color::from_rgba(255, 255, 255, 255),
    );

    draw_text(
        "Type 'play' to start a new game, 'quit' to exit",
        20.0,
        50.0,
        20.0,
        Color::from_rgba(255, 255, 255, 255),
    );

    let input_box_width = screen_width - 20.0;
    let input_box_height = 30.0;
    let input_box_x = 10.0;
    let input_box_y = screen_height - input_box_height - 10.0;

    draw_rectangle(
        input_box_x,
        input_box_y,
        input_box_width,
        input_box_height,
        Color::from_rgba(255, 255, 255, 255),
    );

    draw_text(
        &input,
        input_box_x + 5.0,
        input_box_y + 20.0,
        20.0,
        Color::from_rgba(0, 0, 0, 255),
    );
}

fn create_enemy_vector(world : &mut World) -> Vec<Enemy>
{
    // 3 (5hp) at (33, 20)
    // 3 (10hp) at (20, 60)
    // 4 (20hp) at (130, 25)
    // 1 (50hp) at (61, 59)
    let smol_nmi = (vec2(33., 20.), 5);
    let mild_nmi = (vec2(20., 60.), 10);
    let solid_nmi = (vec2(130., 25.), 20);
    let boss_nmi = (vec2(61., 59.), 50);
    let mut world_enemies = Vec::new();

    for _ in 0..3
    {
        world_enemies.push(smol_nmi.clone());
    }

    for _ in 0..5
    {
        world_enemies.push(mild_nmi.clone());
    }
    
    for _ in 0..4
    {
        world_enemies.push(solid_nmi.clone());
    }


    world_enemies.push(boss_nmi.clone());

    let enemy_vector = Enemy::create_enemy(world, world_enemies);
    
    enemy_vector
}

#[macroquad::main("Giam v0.01")]
async fn main() 
{

    let mut game_state = GameState::Menu;
    let mut input = String::new();
    let _c_state = vec2(0., 0.);

    let _screen_width = screen_width();
    let _screen_height = screen_height();

    let background_texture = load_texture("assets/background.png").await.unwrap();
    let background_texture_dead = load_texture("assets/death.png").await.unwrap(); 
    let fire_texture = load_texture("assets/smoke.png").await.unwrap();
    let ferris_texture = load_texture("assets/ferris.png").await.unwrap();

    let (mut world, camera, map, mut treasure) = level_one::level_one_load_2().await;

    let mut game_quests = QuestLog { quests : vec!()};
    let _ = &game_quests.init();

    let mut user_character = Character {
        hp:255,
        mp:0,
        turn_angle:0,
        attack_damage: 1,
        sprite:"Wizar".to_string(),
        action:CharacterActionState::Idle,action_frame:0,
        attack_selector:0,
        collider:world.add_actor(vec2(16.,16.),1,1),
        attack_collider:world.add_actor(vec2(18.,16.),0,0),
        next_final_pos:vec2(0.,0.),
        sprite_displacement:vec2(0.,0.),
        knockback_frames: 0,
        knocked_back:false,
        last_frame_smoothed:false, 
        move_ordered: false,
        };

    let mut flying_emitter_local = Emitter::new(EmitterConfig {
        local_coords: true,
        texture: Some(fire_texture.clone()),
        ..smoke()
    });

    let mut last = (5., 27.);
    // let mut nmi_vec = Vec::<Enemy>::new();
    let mut treasure_vec = Vec::<Enemy>::new();

    let mut nmi_vec = create_enemy_vector(&mut world);
    treasure_vec.push(treasure.clone());

    loop 
    {
        clear_background(Color::from_rgba(0, 0, 0, 0));

        match game_state {
            GameState::Menu => {
                main_menu(&background_texture.clone(), &mut input);

                flying_emitter_local.draw(vec2(410., 380.));

                let keys_pressed = get_keys_pressed();

                if !keys_pressed.is_empty() {
                    if is_key_pressed(KeyCode::Backspace) {
                        input.pop();
                    } else if is_key_pressed(KeyCode::Space) {
                        input.push(' ');
                    } else if is_key_pressed(KeyCode::Enter) {
                        match input.as_str() {
                            "PLAY" => game_state = GameState::Game,
                            "QUIT" => {
                                break;
                            }
                            _ => {}
                        }
                        input.clear();
                    } else {
                        // println!("{:?}", get_keys_pressed());
                        format!("Please enjoy this fine piece of engineering");
                        let key = get_last_key_pressed().unwrap();
                        let kf = format!("{:?}", key);
                        let key_char = kf.chars().nth(0).unwrap_or('F');
                        // println!("Got keychar : {:?}", kf);
                        input.push(key_char);
                    }
                }
            }
            GameState::Game => {
                // Game logic goes here

                last = level_one_draw(
                    &background_texture,
                    &ferris_texture,
                    &mut user_character,
                    &map,
                    &camera,
                    &mut world,
                    last,
                    &mut nmi_vec,
                    &mut game_quests,
                    &mut treasure_vec,
                    &mut game_state
                )
                .await;

                set_default_camera();


                if is_key_down(macroquad::input::KeyCode::Tab)
                {
                    game_quests.render(_screen_width, _screen_height);
                }

                let hp_str = format!("HP : {:?}", user_character.hp);
                draw_text(&hp_str, 5.0, 20.0, 20.0, Color::from_rgba(0, 0, 0, 255));

                let user_position = world.actor_pos(user_character.collider);
                let position_text = format!("({:?}, {:?})", user_position.x, user_position.y);
                draw_text(&position_text, 5.0, 40.0, 20.0, Color::from_rgba(0, 0, 0, 255));
            }
            GameState::Flag => {
                let flag = misc::do_a_barrel_roll(&background_texture);
                let sentence = format!("Congratz ! the flag is Hero{{{}}}", flag);
                println!("I'm nice -> {:?}", sentence);
                image_menu(&background_texture, &sentence);
            }
            GameState::Dead => {
                image_menu(&background_texture_dead, "You are dead !");
            }

        }

        next_frame().await;
        // sleep(Duration::from_millis(100));
    }


}

enum GameState {
    Menu,
    Game,
    Flag,
    Dead
}
