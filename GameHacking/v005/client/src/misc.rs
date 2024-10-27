use rand::prelude::*;

// Thanks GPT o1
pub fn random_point_in_outer_square() -> (f64, f64) 
{
    // Define the outer square boundaries
    let xmin = 0.0;
    let xmax = 149.;
    let ymin = 0.0;
    let ymax = 99.;

    // Define the inner square thresholds
    let x_lower_threshold = 10.;
    let x_upper_threshold = 90.;
    let y_lower_threshold = 10.;
    let y_upper_threshold = 139.;

    // Compute areas of the four rectangles
    let left_area = (x_lower_threshold - xmin) * (ymax - ymin);
    let right_area = (xmax - x_upper_threshold) * (ymax - ymin);
    let bottom_area = (x_upper_threshold - x_lower_threshold) * (y_lower_threshold - ymin);
    let top_area = (x_upper_threshold - x_lower_threshold) * (ymax - y_upper_threshold);

    let total_area = left_area + right_area + bottom_area + top_area;

    // Compute cumulative probabilities
    let left_prob = left_area / total_area;
    let right_prob = right_area / total_area;
    let bottom_prob = bottom_area / total_area;
    let top_prob = top_area / total_area;

    let left_cum_prob = left_prob;
    let right_cum_prob = left_cum_prob + right_prob;
    let bottom_cum_prob = right_cum_prob + bottom_prob;
    // No need for top_cum_prob since it will be 1.0

    let mut rng = rand::thread_rng();
    let r: f64 = rng.gen(); // Generates a random number between 0.0 and 1.0

    let point = if r < left_cum_prob {
        // Left rectangle
        let x = rng.gen_range(xmin..x_lower_threshold);
        let y = rng.gen_range(ymin..ymax);
        (x.round(), y.round())
    } else if r < right_cum_prob {
        // Right rectangle
        let x = rng.gen_range(x_upper_threshold..xmax);
        let y = rng.gen_range(ymin..ymax);
        (x.round(), y.round())
    } else if r < bottom_cum_prob {
        // Bottom rectangle
        let x = rng.gen_range(x_lower_threshold..x_upper_threshold);
        let y = rng.gen_range(ymin..y_lower_threshold);
        (x.round(), y.round())
    } else {
        // Top rectangle
        let x = rng.gen_range(x_lower_threshold..x_upper_threshold);
        let y = rng.gen_range(y_upper_threshold..ymax);
        (x.round(), y.round())
    };

    point
}
