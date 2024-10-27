use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufRead},
    path::Path, thread::spawn,
};

use lazy_static::lazy_static;
use macroquad::{
    camera::{set_camera, set_default_camera, Camera2D}, color::Color, file::load_string, input::is_key_down, math::{vec2, Rect}, shapes::draw_rectangle, texture::{load_texture, Texture2D}, window::{screen_height, screen_width}
};
use macroquad_platformer::{Actor, Tile, World};
use macroquad_tiled as tiled;
use std::sync::Mutex;
use tiled::Map;

use crate::{
    character::{Character, CharacterActionState}, enemy::Enemy, misc::random_point_in_outer_square, questing::QuestLog, GameState
};

// lol
lazy_static! {
    static ref TEXTURES: Mutex<HashMap<String, Texture2D>> = Mutex::new(HashMap::new());
}

/// Handles the player controls
pub fn handle_controls(character_state: &mut Character, world: &mut World) 
{
    if is_key_down(macroquad::input::KeyCode::W) 
    {
        character_state.sprite_displacement.y -= 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 180;
    }
    if is_key_down(macroquad::input::KeyCode::S) {
        character_state.sprite_displacement.y += 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 0;
    }
    if is_key_down(macroquad::input::KeyCode::A) {
        character_state.sprite_displacement.x -= 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 270;
    }
    if is_key_down(macroquad::input::KeyCode::D) {
        character_state.sprite_displacement.x += 0.1;
        character_state.last_frame_smoothed = false;

        character_state.turn_angle = 90;
    }

    if is_key_down(macroquad::input::KeyCode::Space) {
        character_state.action = CharacterActionState::Attacking;
    }
}


/// So if you're reading this terrible code and know a way of doing this via strings stored in a text file,
/// please feel free to contact me
pub async fn level_one_load_2() -> (World, Camera2D, Map, Enemy) {
    let level_map = load_string("assets/forest_v2.tmj").await.unwrap();

    let tilemap_flat = load_texture("assets/Tilemap_Flat.png").await.unwrap();
    let tilemap_elevation = load_texture("assets/Tilemap_Elevation.png")
        .await
        .unwrap();
    let water = load_texture("assets/Water.png").await.unwrap();
    let foam = load_texture("assets/Foam.png").await.unwrap();
    let _House_Destroyed = load_texture("assets/House_Destroyed.png")
        .await
        .unwrap();
    let thepack = load_texture("assets/thepack.png").await.unwrap();
    let house_blue = load_texture("assets/House_Blue.png").await.unwrap();
    let tilesets_and_props_demo = load_texture("assets/Tilesets and props Demo.png")
        .await
        .unwrap();
    let bridge_All = load_texture("assets/Bridge_All.png").await.unwrap();
    let pumpkin = load_texture("assets/Pumpkin.png").await.unwrap();
    let scarecrow = load_texture("assets/Scarecrow.png").await.unwrap();
    let tileset_grassland_props = load_texture("assets/tileset-grassland-props.png")
        .await
        .unwrap();
    let bush_big = load_texture("assets/Bush_big.png").await.unwrap();
    let mushroom_big = load_texture("assets/Mushroom_big.png").await.unwrap();
    let tree = load_texture("assets/Tree.png").await.unwrap();
    let tx_Struct = load_texture("assets/TX Struct.png").await.unwrap();
    let tx_Props = load_texture("assets/TX Props.png").await.unwrap();
    let tx_Tileset_Wall = load_texture("assets/TX Tileset Wall.png")
        .await
        .unwrap();
    let danger = load_texture("assets/Danger.png").await.unwrap();
    let tower_Destroyed = load_texture("assets/Tower_Destroyed.png")
        .await
        .unwrap();
    let castle_Blue = load_texture("assets/Castle_Blue.png").await.unwrap();
    let rock_mid = load_texture("assets/Rock_mid.png").await.unwrap();
    let house_Destroyed = load_texture("assets/House_Destroyed.png")
        .await
        .unwrap();
    let warrior_Yellow = load_texture("assets/Warrior_Yellow.png")
        .await
        .unwrap();
    let torch_blue = load_texture("assets/Torch_Blue.png").await.unwrap();
    let torch_blue_damaged = load_texture("assets/Torch_Blue_Damaged.png")
        .await
        .unwrap();

    let torch_red = load_texture("assets/Torch_Red.png").await.unwrap();
    let torch_red_damaged = load_texture("assets/Torch_Red_Damaged.png")
        .await
        .unwrap();
    let wizar = load_texture("assets/Wizar.png").await.unwrap();
    let wizar_damaged = load_texture("assets/Wizar_Damaged.png").await.unwrap();
    let map = tiled::load_map(
        &level_map,
        &[
            ("Tilemap_Flat.png", tilemap_flat),
            ("Tilemap_Elevation.png", tilemap_elevation),
            ("Water.png", water),
            ("Foam.png", foam),
            ("thepack.png", thepack),
            ("House_Blue.png", house_blue),
            ("Tilesets and props Demo.png", tilesets_and_props_demo),
            ("Bridge_All.png", bridge_All),
            ("Pumpkin.png", pumpkin),
            ("Scarecrow.png", scarecrow),
            ("tileset-grassland-props.png", tileset_grassland_props),
            ("Bush_big.png", bush_big),
            ("Mushroom_big.png", mushroom_big),
            ("Tree.png", tree),
            ("TX Struct.png", tx_Struct),
            ("TX Props.png", tx_Props),
            ("TX Tileset Wall.png", tx_Tileset_Wall),
            ("Danger.png", danger),
            ("Tower_Destroyed.png", tower_Destroyed),
            ("Castle_Blue.png", castle_Blue),
            ("Rock_mid.png", rock_mid),
            ("House_Destroyed.png", house_Destroyed),
            ("Warrior_Yellow.png", warrior_Yellow),
            ("Torch_Blue.png", torch_blue),
            ("Torch_Blue_Damaged.png", torch_blue_damaged),
            ("Torch_Red.png", torch_red),
            ("Torch_Red_damaged.png", torch_red_damaged),
            ("Wizar.png", wizar),
            ("Wizar_Damaged.png", wizar_damaged),
        ],
        &[],
    )
    .unwrap();

    let mut world = World::new();

    let mut static_colliders = vec![];

    for (_x, _y, tile) in map.tiles("Edges", None) 
    {
        static_colliders.push(if tile.is_some() 
        {
            world.add_solid(vec2((_x) as f32, (_y) as f32), 1, 1);
            Tile::Solid
        } else {
            Tile::Empty
        });

    }

    let _screen_width = screen_width();
    let _screen_height = screen_height();
    let camera = Camera2D::from_display_rect(Rect::new(0.0, 40., 40., -40.));

    let d = init_treasure_quest(&mut world).await;

    (world, camera, map, d)
}

pub async fn init_treasure_quest(world: &mut World) -> Enemy
{

    let treasure_position = random_point_in_outer_square();
    let treasure_position_vector = vec2(treasure_position.0 as f32, treasure_position.1 as f32);
    let treasure_character = Character {
        hp: 1,
        mp: 0,
        turn_angle: 0,
        attack_damage: 0,
        action: CharacterActionState::Idle,
        action_frame: 0,
        attack_selector: 0,
        collider: world.add_actor(treasure_position_vector, 4, 6),
        // collider:world.add_actor(vec2(20.,20.),1,1),
        sprite: "Foam".to_string(),
        attack_collider: world.add_actor(treasure_position_vector, 1, 1),
        // attack_collider: world.add_actor(vec2(20.,20.), 1, 1),

        next_final_pos: treasure_position_vector,
        sprite_displacement: vec2(0., 0.),
        knockback_frames: 0,
        knocked_back: false,
        last_frame_smoothed: false,
        move_ordered: false,
    };

    let treasure_entity = Enemy {
        char: treasure_character,
        move_delta: vec2(0., 0.),
        move_frame: 0,
    };

    treasure_entity
}

/// The treasure is a 1hp enemy we don't draw
pub async fn sunkun_treasure_quest(treasure : &mut Vec<Enemy>, quests: &mut QuestLog)
{
    for tr in treasure.iter_mut()
    {
        if tr.char.hp == 0
        {
            quests.quests.get_mut(1).unwrap().mark_complete();
        }
        
    }
}

/// Has the player finished the game ?
pub async fn check_game_end(world: &mut World, character_state: &mut Character, quests: &mut QuestLog) -> bool
{
    if world.actor_pos(character_state.collider) == vec2(137., 77.)
    {
        if quests.quests_done()
        {
            return true
        }
    }

    return false
}



/// Draws the map
pub async fn level_one_draw_tiles(map : &Map)
{
    map.draw_tiles(
        "Outmap",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Outmap_2",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Water",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Foam",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );
    map.draw_tiles(
        "Shadow",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Ground",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Ground_darker",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Ground_2",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Objects",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Trees_darker",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );

    map.draw_tiles(
        "Objects2",
        Rect::new(0., 0., 320., 320.),
        Rect::new(0., 0., 320., 320.),
    );
}

/// Main level logic.
/// We handle "eveything" in this, which is executed at every loop
pub async fn level_one_draw(
    _background_texture: &Texture2D,
    _ferris: &Texture2D,
    character_state: &mut Character,
    map: &Map,
    _camera: &Camera2D,
    world: &mut World,
    from: (f32, f32),
    spawned_enemies: &mut Vec<Enemy>,
    quests: &mut QuestLog,
    treasure : &mut Vec<Enemy>,
    game_state : &mut GameState
) -> (f32, f32) {

    let _screen_width = screen_width();
    let _screen_height = screen_height();

    handle_controls(character_state, world);

    let player_position = world.actor_pos(character_state.collider);

    let x_delta = from.0 - (player_position.x - 11.);
    let y_delta = from.1 - (player_position.y + 11.);

    let xpos = if x_delta > 1. 
    {
        -0.1
    } else if x_delta < -1. {
        0.1
    } else {
        0.0
    };

    let ypos = if y_delta > 1. 
    {
        -0.1
    } else if y_delta < -1. {
        0.1
    } else {
        0.0
    };

    let nc = Camera2D::from_display_rect(Rect::new(from.0 + xpos, from.1 + ypos, 22., -22.));

    set_camera(&nc);

    level_one_draw_tiles(map).await;

    let pos = world.actor_pos(character_state.collider);

    // Enemies
    let mut dead_count = 0;
    for nmi in spawned_enemies.iter_mut() {
        
        if nmi.char.hp <= 0
        {
            dead_count += 1;
            continue;
        }
        
        let nmipos = world.actor_pos(nmi.char.collider);

        nmi.move_routine(world);
        nmi.aggro(world,character_state);

        nmi.char.apply_displacement(world);
        nmi.char.position_smoother(world).await;

        nmi.char.draw_character(&map, nmipos);

        if nmi.char.action == CharacterActionState::Damaging
        {
            nmi.char.attack_one(character_state, world).await; 
            nmi.char.action = CharacterActionState::Idle;
        }
        
        // println!("Enemy drawn at {:?}", nmipos);
    }

    sunkun_treasure_quest(treasure, quests).await;

    for tr in treasure.iter_mut()
    {
        tr.char.draw_character(&map, vec2(20., 20.));
    }

    if dead_count == spawned_enemies.len()
    {
        quests.quests.get_mut(0).unwrap().mark_complete();
    }


    if character_state.action == CharacterActionState::Damaging {
        character_state.attack(spawned_enemies, world).await;
        character_state.attack(treasure, world).await;
        character_state.action = CharacterActionState::Idle;
    }

    if character_state.hp <= 0
    {
        *game_state = GameState::Dead;
    }
    
    if check_game_end(world, character_state, quests).await
    {
        *game_state = GameState::Flag;
    }

    treasure.get_mut(0).unwrap().move_routine(world);
    character_state.apply_displacement(world);
    character_state.position_smoother(world).await;
    character_state.draw_character(&map, pos);

    (from.0 + xpos, from.1 + ypos)
}
