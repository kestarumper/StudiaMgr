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

fn timeslot_result(node_probabilities: &Vec<f64>, probability: &f64) -> TimeSlotStatus {
    let number_of_broadcasts = node_probabilities
        .into_iter()
        .map(|p| probability > p)
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

fn one_slot(n: usize) -> Vec<f64> {
    let mut rng = rand::thread_rng();
    return (0..n).map(|_| rng.gen::<f64>()).collect();
}

fn scenario_1(n: usize, p: f64) -> u32 {
    let mut slot = 1;
    let result = loop {
        let data: Vec<f64> = one_slot(n);
        let timeslot = timeslot_result(&data, &p);
        if timeslot == TimeSlotStatus::SINGLE {
            break slot;
        }
        slot += 1;
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
                .default_value("1000")
                .help("Number of samples"),
        )
        .get_matches();

    let n: usize = matches.value_of("nodes").unwrap().parse::<usize>().unwrap();
    let samples: usize = matches
        .value_of("samples")
        .unwrap()
        .parse::<usize>()
        .unwrap();
    let p = 1f64 / n as f64;

    let mut data: Vec<f64> = Vec::new();
    let mut max: u32 = 0;
    for _ in 1..samples {
        let selected_in: u32 = scenario_1(n, p);
        if max < selected_in {
            max = selected_in;
        }
        data.push(selected_in as f64);
    }

    let h = Histogram::from_slice(data.as_slice(), Bins::Count(max as usize))
        .style(Style::new().fill("red"));
    let v = ContinuousView::new().add(&h);
    Page::single(&v).save("histogram.svg").expect("saving svg");
    println!("{}", Page::single(&v).dimensions(60, 15).to_text().unwrap());
}
