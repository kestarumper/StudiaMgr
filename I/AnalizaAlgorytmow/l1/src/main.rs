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

fn scenario_2(n: usize, u: f64) -> u32 {
    let mut slot = 0;
    let mut result = 0;
    let round_len: i32 = u.log2().ceil() as i32;
    result = loop {
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
    return result;
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
                .possible_values(&["2", "3"])
                .default_value("2")
                .help("Number of samples"),
        )
        .arg(
            Arg::with_name("supremum")
                .long("supremum")
                .takes_value(true)
                .requires("scenario")
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
    for _ in 1..samples {
        let selected_in: u32 = match scenario_arg {
            2 => scenario_1(n, 1f64 / n as f64),
            3 => scenario_2(n, u),
            _ => panic!("Invalid scenario"),
        };
        if max < selected_in {
            max = selected_in;
        }
        data.push(selected_in as f64);
    }

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
