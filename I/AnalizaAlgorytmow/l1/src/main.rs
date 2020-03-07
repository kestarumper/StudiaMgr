use clap::{App, Arg};
use plotlib::histogram::{Bins, Histogram, Style};
use plotlib::page::Page;
use plotlib::style::Bar;
use plotlib::view::ContinuousView;
use rand::Rng;

#[derive(Debug, PartialEq)]
enum TimeSlotStatus {
    NULL,
    SINGLE,
    COLLISION,
}

struct Pair(f64, f64);

fn timeslot_result(node_probabilities: &Vec<Pair>) -> TimeSlotStatus {
    let number_of_broadcasts =
        node_probabilities
            .into_iter()
            .map(|p| p.1 > p.0)
            .fold(0, |acc, curr| match curr {
                true => acc + 1,
                false => acc,
            });

    let timeslot = match number_of_broadcasts {
        0 => TimeSlotStatus::NULL,
        1 => TimeSlotStatus::SINGLE,
        _ => TimeSlotStatus::COLLISION,
    };
    return timeslot;
}

fn one_slot(n: usize, map_fn: &dyn Fn() -> f64) -> Vec<Pair> {
    let mut rng = rand::thread_rng();
    return (0..n).map(|_| Pair(rng.gen::<f64>(), map_fn())).collect();
}

fn scenario_1(n: usize, p: f64) -> u32 {
    let mut slot = 1;
    let result = loop {
        let data: Vec<Pair> = one_slot(n, &|| p);
        let timeslot = timeslot_result(&data);
        if timeslot == TimeSlotStatus::SINGLE {
            break slot;
        }
        slot += 1;
    };
    return result;
}

fn scenario_2(n: usize, u: f64) -> (u32, u32) {
    let mut slot = 0;
    let mut round = 0;
    let mut result = 0;
    let round_len: i32 = u.log2().ceil() as i32;
    result = loop {
        round += 1;
        for i in 1..round_len {
            slot += 1;
            let data: Vec<Pair> = one_slot(n, &|| 1f64 / 2f64.powi(i as i32));
            let timeslot = timeslot_result(&data);
            if timeslot == TimeSlotStatus::SINGLE {
                result = slot;
                break;
            }
        }
        if result > 0 {
            break result;
        }
    };
    return (result, round);
}

fn expected_value(data: &Vec<f64>) -> f64 {
    let sum: f64 = data.into_iter().sum();
    return sum / data.len() as f64;
}

fn variance(data: &Vec<f64>, ex: f64) -> f64 {
    return data.into_iter().map(|v| (v - ex).powi(2)).sum::<f64>() / data.len() as f64;
}

fn main() {
    let matches = App::new("Leader choice")
        .version("0.1.0")
        .author("Adrian Mucha <kestarumper8@gmail.com>")
        .about("Leadership problem")
        .arg(
            Arg::with_name("nodes")
                .short("n")
                .long("nodes")
                .takes_value(true)
                .required(true)
                .help("Number of nodes"),
        )
        .arg(
            Arg::with_name("samples")
                .short("s")
                .long("samples")
                .takes_value(true)
                .required(true)
                .help("Number of samples"),
        )
        .arg(
            Arg::with_name("scenario")
                .long("scenario")
                .takes_value(true)
                .possible_values(&["2", "3"])
                .required(true)
                .help("Select scenario"),
        )
        .arg(
            Arg::with_name("supremum")
                .long("supremum")
                .takes_value(true)
                .required_if("scenario", "3")
                .help("Supremum"),
        )
        .get_matches();

    let n: usize = matches.value_of("nodes").unwrap().parse::<usize>().unwrap();
    let samples: usize = matches
        .value_of("samples")
        .unwrap()
        .parse::<usize>()
        .unwrap();
    let scenario_arg = matches
        .value_of("scenario")
        .unwrap()
        .parse::<usize>()
        .unwrap();
    let u: f64 = matches
        .value_of("supremum")
        .unwrap_or("0")
        .parse::<f64>()
        .unwrap();

    let mut data: Vec<f64> = Vec::new();
    let mut max: u32 = 0;
    let mut total_rounds = 0;
    for _ in 1..samples {
        let selected_in: u32;
        if scenario_arg == 2 {
            selected_in = scenario_1(n, 1f64 / n as f64);
        } else if scenario_arg == 3 {
            let (a, b) = scenario_2(n, u);
            selected_in = a;
            total_rounds += b;
        } else {
            panic!("Invalid scenario");
        }
        if max < selected_in {
            max = selected_in;
        }
        data.push(selected_in as f64);
    }

    let lambda: f64 = samples as f64 / total_rounds as f64;
    let ex = expected_value(&data);
    let varx = variance(&data, ex);
    let p: f64 = 1f64 / ex;
    println!(
        "EX={}, VarX={}, VarX2={}, Lambda={}",
        ex,
        varx,
        (1f64 - p) / p.powi(2),
        lambda
    );

    let h = Histogram::from_slice(data.as_slice(), Bins::Count(max as usize))
        .style(Style::new().fill("red"));
    let v = ContinuousView::new().add(&h);
    Page::single(&v)
        .save(format!(
            "histogram_n={}_s={}_v={:?}.svg",
            n,
            samples,
            (scenario_arg, u)
        ))
        .expect("saving svg");
    println!("{}", Page::single(&v).dimensions(60, 15).to_text().unwrap());
}
