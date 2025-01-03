#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// ���庯�� threeSum ����Ѱ�Һ�ΪĿ��ֵ����Ԫ��
vector<vector<int>> threeSum(vector<int>& nums, int target) {
    vector<vector<int>> result;  // ���ڴ洢������������Ԫ��

    // ������������������
    sort(nums.begin(), nums.end());

    // ��������
    for (int i = 0; i < nums.size() - 2; i++) {
        // �����ǰ������ǰһ��������ͬ�������˴�ѭ��
        if (i > 0 && nums[i] == nums[i - 1]) {
            continue;
        }

        int left = i + 1;  // ��ָ��
        int right = nums.size() - 1;  // ��ָ��

        // ����ָ��С����ָ��ʱ��ִ�����²���
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];  // ���㵱ǰ�������ֵĺ�

            // ����͵���Ŀ��ֵ
            if (sum == target) {
                // ����Ԫ����ӵ������
                result.push_back({ nums[i], nums[left], nums[right] });

                // ������ָ��ָ����ظ�����
                while (left < right && nums[left] == nums[left + 1]) {
                    left++;
                }
                // ������ָ��ָ����ظ�����
                while (left < right && nums[right] == nums[right - 1]) {
                    right--;
                }
                // ��ָ�����ƣ���ָ�����ƣ�����Ѱ���������ܵ���Ԫ��
                left++;
                right--;
            }
            // �����С��Ŀ��ֵ����ָ������
            else if (sum < target) {
                left++;
            }
            // ����ʹ���Ŀ��ֵ����ָ������
            else {
                right--;
            }
        }
    }

    // ���������ҵ�����Ԫ��
    return result;
}

int main() {
    int target, n;
    cin >> target >> n;  // ����Ŀ��ֵ������Ԫ�ظ���

    vector<int> nums(n);  // �����洢����Ԫ�ص�����
    for (int i = 0; i < n; i++) {
        cin >> nums[i];  // ��������Ԫ��
    }

    vector<vector<int>> res = threeSum(nums, target);  // ���ú�����ȡ���

    // �������������������Ԫ��
    for (const auto& triplet : res) {
        cout << triplet[0] << " " << triplet[1] << " " << triplet[2] << endl;
    }

    return 0;
}