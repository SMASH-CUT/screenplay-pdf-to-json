export interface ILineParse {
  text: string;
  x: number;
  y: number;
}

export interface IFinalParse {
  page: number;
  content: ILineParse[];
}
