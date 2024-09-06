Morris.Line({
  //Контейнер для вывода графика
  element: 'myfirstchart',
  //Данные для графика
  data: [
      { y: '2008', oil: 144, ruble: 24.48 },
      { y: '2009', oil: 41,  ruble: 28.26 },
      { y: '2010', oil: 80,  ruble: 29.59 },
      { y: '2011', oil: 94,  ruble: 30.60 },
      { y: '2012', oil: 124, ruble: 31.22 },
      { y: '2013', oil: 115, ruble: 30.42 },
      { y: '2014', oil: 105, ruble: 33.15 },
      { y: '2015', oil: 56,  ruble: 56.49 },
      { y: '2016', oil: 36,  ruble: 75.95 }
  ],
  xkey: 'y',

  //Префикс в конце для оси Y
  postUnits:' H/s',

  //Коридор цены за 1 доллар
  goals:[45.0, 27.0],
  goalStrokeWidth:2,
  goalLineColors:['#d9534f'],

  //Событийные линии по оси X
  events: ['2014-01-01', '2015-10-01'],
  eventStrokeWidth:2,
  eventLineColors:['#428bca'],

  //Цвет линий
  lineColors:['#5cb85c','#f0ad4e'],
  //Выводимые линии
  ykeys: ['oil', 'ruble'],
  //Названия линий
  labels: ['Нефть', 'Рубль']
});