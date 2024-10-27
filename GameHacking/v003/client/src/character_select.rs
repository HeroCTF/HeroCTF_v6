use macroquad::{
    color::Color,
    math::vec2,
    texture::{draw_texture_ex, DrawTextureParams, Texture2D},
};

pub fn character_selection_draw(background_texture: &Texture2D) {
    let params = DrawTextureParams {
        dest_size: Some(vec2(200., 200.)),
        ..DrawTextureParams::default()
    };

    draw_texture_ex(
        &background_texture,
        50.0,
        50.0,
        Color::from_rgba(255, 255, 255, 255),
        params.clone(),
    );

    draw_texture_ex(
        &background_texture,
        250.0,
        50.0,
        Color::from_rgba(255, 255, 255, 255),
        params.clone(),
    );

    draw_texture_ex(
        &background_texture,
        350.0,
        50.0,
        Color::from_rgba(255, 255, 255, 255),
        params,
    );
}
