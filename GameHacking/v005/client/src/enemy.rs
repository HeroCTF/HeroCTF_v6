use crate::character::{Character, CharacterActionState};
use macroquad::math::{vec2, Vec2};
use macroquad_platformer::World;
use rand::{thread_rng, Rng};

/// Enemy is just a character with handled movement.
/// Wow, such AI !
#[derive(Debug, PartialEq, Clone)]
pub struct Enemy 
{
    pub char: Character,
    pub move_delta: Vec2,
    pub move_frame: u16,
}

impl Enemy 
{

    pub fn partial_serialize(&self) -> Vec<u8>
    {
        let mut serialized_vec = Vec::new();
        serialized_vec.push(self.char.mp);
        serialized_vec.push(self.char.hp);
        serialized_vec.push(self.char.attack_damage);

        serialized_vec
    }

    /// Creates an enemy from a position and a sprite
    pub fn make_enemy(world: &mut World, position: Vec2, sprite: String) -> Enemy 
    {
        let mut attack_collider = position;
        attack_collider.y += 2.;

        let enemy_char = Character {
            hp: 5,
            mp: 0,
            turn_angle: 0,
            attack_damage: 1,
            action: CharacterActionState::Idle,
            action_frame: 0,
            attack_selector: 0,
            collider: world.add_actor(position, 4, 6),
            sprite: sprite,
            attack_collider: world.add_actor(attack_collider, 0, 0),
            next_final_pos: vec2(0.,0.),
            sprite_displacement: vec2(0., 0.),
            knocked_back: false,
            knockback_frames: 0,
            last_frame_smoothed: false,
            move_ordered: false,
        };

        Enemy {
            char: enemy_char,
            move_delta: vec2(0., 0.),
            move_frame: 0,
        }
    }

    /// Creates a vector of enemies from a vector containing their initial positions and HP
    pub fn create_enemy(world: &mut World, positions_and_hp: Vec<(Vec2, u8)>) -> Vec<Enemy> {
        let mut enemies = Vec::new();

        let mut id = 0u8;

        for (position, hp) in positions_and_hp 
        {
            let sprite = {
                if hp >= 5
                {
                    "Torch_Red"
                }
                else {
                    "Torch_Blue"
                }
            };

            let mut enemy = Enemy::make_enemy(world, position, sprite.to_string());
            enemy.char.hp = hp;
            enemy.char.mp = id;
            id += 1;


            let serialized_enemy = enemy.partial_serialize();


            enemies.push(enemy);
        }
        enemies
    }

    /// Wow that AI is so good (it's not)
    pub fn move_routine(&mut self, world: &mut World) 
    {
        self.char.last_frame_smoothed = false;

        let current_position = world.actor_pos(self.char.collider);

        if self.move_delta == vec2(0., 0.) 
        {
            if self.move_frame < 15
            {
                self.move_frame += 1;
                return;

            }

            // println!("Move routine: generating position");
            loop 
            {
                self.move_frame = 0;
                let mut rng = thread_rng();
                let next_position_xdelta = rng.gen_range(-5..5) as f32;
                let next_position_ydelta = rng.gen_range(-5..5) as f32;
                let next_position_delta = vec2(next_position_xdelta, next_position_ydelta);

                let next_position = current_position + next_position_delta;

                if !world.solid_at(next_position) 
                {
                    self.move_delta = next_position_delta;
                    // println!("Next delta move : {:?}", next_position_delta);
                    break;
                }
            }
        }
        // current_position != next_final_pos
        else 
        {
            self.char.sprite_displacement.x += 
            {
                if self.move_delta.x.abs() >= 0.05 
                {
                    if self.move_delta.x > 0. 
                    {
                        self.move_delta.x -= 0.05;
                        -0.05
                    } else {
                        self.move_delta.x += 0.05;
                        0.05
                    }
                } else {
                    let to_move = -self.move_delta.x;
                    self.move_delta.x = 0.;
                    to_move
                }
            };

            self.char.sprite_displacement.y += {
                if self.move_delta.y.abs() >= 0.05 
                {
                    if self.move_delta.y > 0. 
                    {
                        self.move_delta.y -= 0.05;
                        -0.05
                    } else {
                        self.move_delta.y += 0.05;
                        0.05
                    }
                } else {
                    let to_move = -self.move_delta.y;
                    self.move_delta.y = 0.;
                    to_move
                }
            };
        }
    }

    pub fn aggro(&mut self, world : &mut World, target : &mut Character)
    {
        let self_position = world.actor_pos(self.char.collider);
        let target_position = world.actor_pos(target.collider);

        let distance = self_position.distance(target_position);

        // Do not aggro if too far
        if distance > 10.
        {
            return
        }

        // Should be in range for attacking
        // There will be a problem with the angle, but let's say it's a feature and mobs can miss attacks lol
        // Also no time nor energy to fix it. 
        if distance < 3.
        {
            self.char.action = CharacterActionState::Attacking;

            return
        }

        // Compute a position where the enemy attack can reach 
        self.char.next_final_pos = target_position;
        // Compute the movement the enemy will have to do to get into position
        let position_delta = target_position - self_position;
        // The movement will be handled by the move_routine()
        // no movement will be added in the routine because the position will not be the next final pos
        self.move_delta = - position_delta;


    }
}