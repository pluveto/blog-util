
let mylist = [1, 2, 3, 4, 5, 3, 4, 1, 6, 7, 8, 7, 8, 9, 7, 8, 9, 5, 4, 5, 4, 2]

let counter = [0,0,0,0]
let myframes = [-1,-1,-1,-1]

function findMinIdx(counter) {
    let min = 256;
    let minIdx = -1;
    for (let i = 0; i < counter.length; i++) {
        const element = counter[i];
        if(element < min){
            min = element;
            minIdx = i;
        }
    }
    return minIdx
}

function printVec({counter, myframes}) {
    var buff = "i\t";
    for (let i = 0; i < counter.length; i++) {        
        buff+= i.toString() + " ";
    }
    buff += "\ncnt\t"
    for (let i = 0; i < counter.length; i++) {
        buff+= counter[i].toString() + " ";
    }
    buff += "\npage\t"
    for (let i = 0; i < myframes.length; i++) {
        buff+= myframes[i].toString() + " ";
    }
    buff +="\n"
    console.log(buff);
}

function hit({counter, myframes, page}) {
    for (let i = 0; i < counter.length; i++) {
        if(myframes[i] == page)
        {
            counter[i] != 7 && counter[i]++;
            return i;
        }
    }
    return -1;
}

function decrease({counter, exceptIdx}) {
    for (let i = 0; i < counter.length; i++) {
        if(exceptIdx != i){
            counter[i] != 0 && counter[i]--;
        }            
    }
}
let faultCounter = 0;
for (let i = 0; i < mylist.length; i++) {
    const page = mylist[i];
    console.log("search ", page);
    var hitIdx = hit({counter, myframes, page})
    // 命中则跳过
    if(hitIdx != -1){
        console.log("hit");
        decrease({counter, hitIdx})
        continue;
    }
    console.log("page fault");
    faultCounter++;
    // miss
    var minIdx = findMinIdx(counter)
    console.log('minIdx',minIdx);
    myframes[minIdx] = page;
    counter[minIdx] = 7;
    decrease({counter, minIdx})
    printVec({counter, myframes})
}

console.log("faultCounter", faultCounter);