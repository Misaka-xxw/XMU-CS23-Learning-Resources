int clock[10];
mintime = 1 << 15
int method_num[10] = {0}, solution_clock[10] = {0}, realmethod[10] = {0};
relation = [
    [0],
    [1, 2, 4, 5],    // 1
    [1, 2, 3],       // 2
    {2, 3, 5, 6},    // 3
    {1, 4, 7},       // 4
    {2, 4, 5, 6, 8}, // 5
    {3, 6, 9},       // 6
    {4, 5, 6, 7},    // 7
    {7, 8, 9},       // 8
    {5, 6, 8, 9}     // 9
};
void dfs(int depth)
{
    if (depth > 9)
    {
        bool all0 = 1;
        int temptime = 0;
        int tempclock[10];
        for (int i = 1; i <= 9; i++)
        {
            tempclock[i] = clock[i];
        }
        for (int i = 1; i <= 9; i++)
        {
            for (auto element : relation[i])
            {
                tempclock[element] = (tempclock[element] + method_num[i]) % 4;
            }
        }
        for (int i = 1; i <= 9; i++)
        {
            if (tempclock[i])
            {
                all0 = 0;
                break;
            }
        }
        if (all0 && temptime < mintime)
        {
            mintime = temptime;
            for (int i = 1; i <= 9; i++)
            {
                realmethod[i] = method_num[i];
                cout<<"ok!";
            }
        }
        return;
    }

    for (int j = 0; j < 4; j++)
    {
        method_num[depth] = j;
        dfs(depth + 1);
    }
    return;
}

int main()
{
    for (int i = 1; i < 10; cin >> clock[i++]);
    dfs(1);
    for(int i=1;i<=9;i++){
        for(int j=realmethod[i];j--;j>0){
            cout<<i<<' ';
        }
    }
    return 0;
}