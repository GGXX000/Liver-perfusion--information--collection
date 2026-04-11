<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <h2>🏥 猪肝脏常温机械灌注数据录入系统</h2>
          </div>
        </template>

        <div class="experiment-section">
          <div style="display: flex; gap: 10px; align-items: center;">
            <el-input 
              v-model="expCode" 
              placeholder="请输入实验编号 (如: NMP-Pig-007)" 
              size="large" 
              style="width: 300px"
              @keyup.enter="confirmExperiment"
            >
              <template #prepend>实验编号</template>
            </el-input>
            <el-button type="primary" size="large" @click="confirmExperiment" :loading="loadingExp">
              {{ currentExp ? '刷新 / 切换实验' : '查询 / 新建实验' }}
            </el-button>
            <el-button type="info" size="large" @click="openExperimentSelector">
              选择已有实验
            </el-button>
            <el-tag v-if="currentExp" type="success" size="large" style="margin-left: 10px;">
              当前操作: {{ currentExp.experiment_code }}
            </el-tag>
          </div>
        </div>

        <el-dialog v-model="showExpSelector" title="选择实验" width="600px">
          <el-table :data="allExperiments" stripe style="width: 100%" height="400" @row-click="selectExperiment">
            <el-table-column prop="experiment_code" label="实验编号" />
            <el-table-column prop="experiment_date" label="创建时间" :formatter="formatDate" />
          </el-table>
        </el-dialog>

        <el-divider border-style="dashed" />

        <div v-if="currentExp">
          <el-tabs type="border-card">

            <el-tab-pane label="📋 基本信息 (Basic Info)">
              <el-form :model="basicForm" label-width="140px" class="input-area">
                
                <!-- [新增] 供体基本信息 -->
                <el-row :gutter="20">
                  <el-col :span="6">
                    <el-form-item label="供体品种">
                      <el-select v-model="basicForm.donor_breed" placeholder="请选择" style="width: 100%">
                        <el-option label="长白猪" value="长白猪" />
                        <el-option label="巴马香猪" value="巴马香猪" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="性别">
                      <el-select v-model="basicForm.gender" placeholder="请选择" style="width: 100%">
                        <el-option label="雄性" value="雄性" />
                        <el-option label="雌性" value="雌性" />
                        <el-option label="阉割" value="阉割" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="月龄">
                      <el-input v-model.number="basicForm.age_months" style="width: 100%" placeholder="请输入">
                        <template #append>月</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="体重">
                      <el-input v-model.number="basicForm.weight_kg" style="width: 100%" placeholder="请输入">
                        <template #append>kg</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="8">
                    <el-form-item label="实验日期">
                      <el-date-picker
                        v-model="basicForm.record_date"
                        type="date"
                        placeholder="点击选择日期"
                        value-format="YYYY-MM-DD"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="总灌注时间">
                      <el-input v-model.number="basicForm.total_duration" style="width: 100%" placeholder="请输入">
                        <template #append>min</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="总胆汁量">
                      <el-input v-model.number="basicForm.total_bile" style="width: 100%" placeholder="请输入">
                        <template #append>ml</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                  <el-col :span="8">
                     <el-form-item label="灌注液体系量">
                      <el-input v-model.number="basicForm.perfusion_liquid_vol" style="width: 100%" placeholder="请输入">
                        <template #append>ml</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="灌注前肝重">
                      <el-input v-model.number="basicForm.liver_weight_pre" style="width: 100%" placeholder="请输入">
                        <template #append>g</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="灌注后肝重">
                      <el-input v-model.number="basicForm.liver_weight_post" style="width: 100%" placeholder="请输入">
                        <template #append>g</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="20">
                   <el-col :span="8">
                    <el-form-item label="冷却血时间">
                      <el-input v-model.number="basicForm.cold_ischemia_time" style="width: 100%" placeholder="请输入">
                        <template #append>min</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item label="热缺血时间">
                      <el-input v-model.number="basicForm.warm_ischemia_time" style="width: 100%" placeholder="请输入">
                        <template #append>min</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <div style="text-align: center; margin-top: 10px;">
                  <el-button type="primary" size="large" @click="submitBasicInfo" style="width: 200px;">
                    {{ editingBasicId ? '保存修改' : '保存基本信息' }}
                  </el-button>
                  <el-button v-if="editingBasicId" size="large" @click="resetBasicForm" style="margin-left: 10px;">取消编辑</el-button>
                </div>
              </el-form>

              <el-divider content-position="left">已保存记录</el-divider>
              <el-table 
                :data="currentExp.basic_infos" 
                stripe 
                border 
                style="width: 100%" 
                height="400"
                :row-class-name="tableRowClassName"
              >
                <el-table-column prop="record_date" label="日期" width="120" fixed="left" sortable />
                <el-table-column prop="donor_breed" label="品种" width="100" />
                <el-table-column prop="gender" label="性别" width="80" />
                <el-table-column prop="age_months" label="月龄(月)" width="100" />
                <el-table-column prop="weight_kg" label="体重(kg)" width="100" />
                <el-table-column prop="total_duration" label="总时间(min)" width="120" />
                <el-table-column prop="total_bile" label="总胆汁(ml)" width="120" />
                <el-table-column prop="perfusion_liquid_vol" label="液体量(ml)" width="120" />
                <el-table-column prop="liver_weight_pre" label="肝重前(g)" width="110" />
                <el-table-column prop="liver_weight_post" label="肝重后(g)" width="110" />
                <el-table-column prop="cold_ischemia_time" label="冷却血(min)" width="120" />
                <el-table-column prop="warm_ischemia_time" label="热缺血(min)" width="120" />
                <el-table-column label="操作" width="140" fixed="right">
                  <template #default="scope">
                    <el-button link type="primary" size="small" @click="editBasicInfo(scope.row)">编辑</el-button>
                    <el-popconfirm title="确定删除吗?" @confirm="deleteBasicInfo(scope.row.id)">
                      <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            
            <el-tab-pane label="🩸 血气分析 (Blood Gas)">
              <el-form :model="bgForm" label-width="110px" class="input-area">
                <!-- 第一行：基础信息 -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="时间点 T=">
                      <el-input v-model="bgForm.record_time" placeholder="请输入">
                         <template #append>h</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="血管">
                      <el-select v-model="bgForm.sample_site" placeholder="请选择">
                        <el-option value="门静脉" label="门静脉" />
                        <el-option value="肝动脉" label="肝动脉" />
                        <el-option value="腔静脉" label="腔静脉" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="酸碱度">
                      <el-input v-model.number="bgForm.ph" placeholder="请输入" style="width:100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="二氧化碳分压">
                      <el-input v-model.number="bgForm.pco2" style="width: 100%" placeholder="请输入">
                        <template #append>mmHg</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第二行：气体与电解质 -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="氧分压">
                      <el-input v-model.number="bgForm.po2" style="width: 100%" placeholder="请输入">
                        <template #append>mmHg</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="钠离子">
                      <el-input v-model.number="bgForm.na" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="钾离子">
                      <el-input v-model.number="bgForm.k" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="氯离子">
                      <el-input v-model.number="bgForm.cl" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第三行：电解质与代谢 -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="钙离子">
                      <el-input v-model.number="bgForm.ca" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="葡萄糖">
                      <el-input v-model.number="bgForm.glu" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="乳酸">
                      <el-input v-model.number="bgForm.lac" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="红细胞压积">
                      <el-input v-model.number="bgForm.hct" style="width: 100%" placeholder="请输入">
                        <template #append>%PCV</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第四行：血红蛋白与酸碱状态 -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="总二氧化碳">
                      <el-input v-model.number="bgForm.tco2" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="血红蛋白">
                      <el-input v-model.number="bgForm.hb" style="width: 100%" placeholder="请输入">
                        <template #append>g/dL</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="碳酸氢根">
                      <el-input v-model.number="bgForm.hco3" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="细胞外碱剩余">
                      <el-input v-model.number="bgForm.be_ecf" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第五行：其他 -->
                <el-row :gutter="10">
                   <el-col :span="6">
                    <el-form-item label="血中碱剩余">
                      <el-input v-model.number="bgForm.be_b" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="氧饱和度">
                      <el-input v-model.number="bgForm.so2" style="width: 100%" placeholder="请输入">
                        <template #append>%</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="阴离子间隙">
                      <el-input v-model.number="bgForm.an_gap" style="width: 100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-button type="primary" @click="submitBloodGas" style="width: 100px;">
                      {{ editingBgId ? '保存修改' : '保存' }}
                    </el-button>
                    <el-button v-if="editingBgId" @click="resetBgForm" style="margin-left: 5px;">取消</el-button>
                  </el-col>
                </el-row>
              </el-form>

              <el-divider content-position="left">已录入的血气数据</el-divider>
              <el-table 
                :data="currentExp.blood_gases" 
                stripe 
                border 
                style="width: 100%" 
                height="300"
                :row-class-name="tableRowClassName"
              >
                <el-table-column prop="record_time" label="时间点(h)" width="100" />
                <el-table-column prop="sample_site" label="血管" width="80" />
                <el-table-column prop="ph" label="酸碱度" width="80" />
                <el-table-column prop="pco2" label="二氧化碳分压" width="120" />
                <el-table-column prop="po2" label="氧分压" width="100" />
                <el-table-column prop="na" label="钠离子" width="80" />
                <el-table-column prop="k" label="钾离子" width="80" />
                <el-table-column prop="cl" label="氯离子" width="80" />
                <el-table-column prop="ca" label="钙离子" width="80" />
                <el-table-column prop="glu" label="葡萄糖" width="80" />
                <el-table-column prop="lac" label="乳酸" width="80" />
                <el-table-column prop="hct" label="红细胞压积" width="100" />
                <el-table-column prop="tco2" label="总二氧化碳" width="110" />
                <el-table-column prop="hb" label="血红蛋白" width="100" />
                <el-table-column prop="hco3" label="碳酸氢根" width="100" />
                <el-table-column prop="be_ecf" label="细胞外碱剩余" width="120" />
                <el-table-column prop="be_b" label="血中碱剩余" width="110" />
                <el-table-column prop="so2" label="氧饱和度(%)" width="110" />
                <el-table-column prop="an_gap" label="阴离子间隙" width="100" />
                <el-table-column label="操作" width="120" fixed="right">
                  <template #default="scope">
                    <el-button link type="primary" size="small" @click="editBloodGas(scope.row)">编辑</el-button>
                    <el-popconfirm title="确定删除吗?" @confirm="deleteBloodGas(scope.row.id)">
                      <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="🧪 生化指标 (Biochem)">
              <el-form :model="bioForm" label-width="140px" class="input-area">
                <!-- 第一行：基础信息 & 肝功能 (酶类) -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="时间点 T=">
                      <el-input v-model="bioForm.record_time" placeholder="请输入">
                        <template #append>h</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                     <el-form-item label="采样部位">
                      <el-select v-model="bioForm.sample_site" placeholder="请选择">
                        <el-option value="门静脉" label="门静脉" />
                        <el-option value="腔静脉" label="腔静脉" />
                      </el-select>
                     </el-form-item>
                  </el-col>
                  <el-col :span="6">
                     <el-form-item label="来源">
                      <el-select v-model="bioForm.sample_source">
                        <el-option value="OnSite" label="现场" />
                        <el-option value="Lab" label="外送" />
                      </el-select>
                     </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="ALT">
                      <el-input v-model.number="bioForm.alt" style="width:100%" placeholder="请输入">
                        <template #append>U/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第二行：肝功能 (酶类 & 蛋白) -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="AST">
                      <el-input v-model.number="bioForm.ast" style="width:100%" placeholder="请输入">
                        <template #append>U/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="白蛋白">
                      <el-input v-model.number="bioForm.alb" style="width:100%" placeholder="请输入">
                        <template #append>g/dL</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="总蛋白">
                      <el-input v-model.number="bioForm.tp" style="width:100%" placeholder="请输入">
                        <template #append>g/dL</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="球蛋白">
                      <el-input v-model.number="bioForm.glob" style="width:100%" placeholder="请输入">
                        <template #append>g/dL</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第三行：肝功能 (胆红素 & 比值) -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="白球比值">
                      <el-input v-model.number="bioForm.ag_ratio" style="width:100%" placeholder="请输入" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="直接胆红素">
                      <el-input v-model.number="bioForm.dbil" style="width:100%" placeholder="请输入">
                        <template #append>umol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="总胆红素">
                      <el-input v-model.number="bioForm.tbil" style="width:100%" placeholder="请输入">
                        <template #append>umol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="葡萄糖">
                      <el-input v-model.number="bioForm.glu" style="width:100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第四行：肾功能 -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="肌酐">
                      <el-input v-model.number="bioForm.crea" style="width:100%" placeholder="请输入">
                        <template #append>umol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="尿酸">
                      <el-input v-model.number="bioForm.ua" style="width:100%" placeholder="请输入">
                        <template #append>umol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="尿素">
                      <el-input v-model.number="bioForm.urea" style="width:100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="尿素/肌酐比值">
                      <el-input v-model.number="bioForm.urea_crea_ratio" style="width:100%" placeholder="请输入" />
                    </el-form-item>
                  </el-col>
                </el-row>

                <!-- 第五行：血脂 -->
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="甘油三酯">
                      <el-input v-model.number="bioForm.tg" style="width:100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="总胆固醇">
                      <el-input v-model.number="bioForm.tc" style="width:100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="高密度脂蛋白">
                      <el-input v-model.number="bioForm.hdl" style="width:100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="低密度脂蛋白">
                      <el-input v-model.number="bioForm.ldl" style="width:100%" placeholder="请输入">
                        <template #append>mmol/L</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row :gutter="10" style="margin-top: 10px; display: flex; justify-content: flex-end;">
                  <el-col :span="4">
                    <el-button type="success" @click="submitBiochem" style="width: 100%;">
                      {{ editingBioId ? '保存修改' : '保存' }}
                    </el-button>
                  </el-col>
                  <el-col :span="4" v-if="editingBioId">
                    <el-button @click="resetBioForm" style="width: 100%;">取消</el-button>
                  </el-col>
                </el-row>
              </el-form>

              <el-divider content-position="left">已录入的生化数据</el-divider>
              <el-table 
                :data="currentExp.biochems" 
                stripe 
                border 
                style="width: 100%" 
                height="300"
                :row-class-name="tableRowClassName"
              >
                <el-table-column prop="record_time" label="时间点" width="100">
                  <template #default="scope">T={{ scope.row.record_time }}h</template>
                </el-table-column>
                <el-table-column prop="sample_source" label="来源" width="80">
                  <template #default="scope">
                    <el-tag :type="scope.row.sample_source === 'Lab' ? 'warning' : 'success'">
                      {{ scope.row.sample_source === 'Lab' ? '外送' : '现场' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="sample_site" label="部位" width="80" />
                <el-table-column prop="alt" label="ALT" width="70" />
                <el-table-column prop="ast" label="AST" width="70" />
                <el-table-column prop="alb" label="白蛋白" width="80" />
                <el-table-column prop="tp" label="总蛋白" width="80" />
                <el-table-column prop="glob" label="球蛋白" width="80" />
                <el-table-column prop="ag_ratio" label="白球比" width="80" />
                <el-table-column prop="tbil" label="总胆红素" width="90" />
                <el-table-column prop="dbil" label="直胆" width="80" />
                <el-table-column prop="crea" label="肌酐" width="80" />
                <el-table-column prop="ua" label="尿酸" width="80" />
                <el-table-column prop="urea" label="尿素" width="80" />
                <el-table-column prop="urea_crea_ratio" label="尿素/肌酐" width="100" />
                <el-table-column prop="glu" label="葡萄糖" width="80" />
                <el-table-column prop="tg" label="甘油三酯" width="90" />
                <el-table-column prop="tc" label="总胆固醇" width="90" />
                <el-table-column prop="hdl" label="HDL" width="80" />
                <el-table-column prop="ldl" label="LDL" width="80" />
                <el-table-column label="操作" width="120" fixed="right">
                  <template #default="scope">
                     <el-button link type="primary" size="small" @click="editBiochem(scope.row)">编辑</el-button>
                     <el-popconfirm title="确定删除吗?" @confirm="deleteBiochem(scope.row.id)">
                      <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="📈 灌注物理参数" name="perfusion">
              <div style="margin-bottom: 20px;">
                 <el-upload
                    class="upload-demo"
                    drag
                    action=""
                    :http-request="uploadPerfusionFile"
                    :show-file-list="false"
                    accept=".xlsx,.xls"
                 >
                    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                    <div class="el-upload__text">
                       将文件拖到此处，或 <em>点击上传</em>
                    </div>
                    <template #tip>
                       <div class="el-upload__tip">
                          只能上传 xlsx/xls 文件，系统将自动解析数据
                       </div>
                    </template>
                 </el-upload>
              </div>

              <el-divider content-position="left">已录入的物理参数文件</el-divider>
              <el-table 
                :data="currentExp.perfusion_files" 
                stripe 
                border 
                style="width: 100%" 
                height="500"
              >
                <el-table-column prop="upload_time" label="上传时间" width="180" />
                <el-table-column prop="filename" label="文件名" />
                <el-table-column prop="status" label="状态" width="100">
                   <template #default="scope">
                      <el-tag :type="scope.row.status === '已转化' ? 'success' : 'danger'">{{ scope.row.status }}</el-tag>
                   </template>
                </el-table-column>
                <el-table-column label="操作" width="250" fixed="right">
                  <template #default="scope">
                     <el-button link type="primary" size="small" @click="viewPerfusionFile(scope.row)">查看</el-button>
                     <el-button link type="primary" size="small" @click="downloadPerfusionJson(scope.row)">转化JSON</el-button>
                     <el-popconfirm title="确定删除吗? 同时会删除相关数据" @confirm="deletePerfusionFile(scope.row.id)">
                      <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="📊 统计信息" name="stat">
              <el-form :model="statForm" label-width="120px" class="input-area">
                <el-row :gutter="10">
                  <el-col :span="6">
                    <el-form-item label="术前禁食时间">
                      <el-input v-model.number="statForm.fasting_time" placeholder="请输入" style="width: 100%">
                         <template #append>h</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="麻醉方式">
                      <el-input v-model="statForm.anesthesia_method" placeholder="请输入" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="肝素化剂量">
                      <el-input v-model.number="statForm.heparin_dosage" placeholder="请输入" style="width: 100%">
                         <template #append>mg/kg</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="取肝时间">
                      <el-time-picker v-model="statForm.acquisition_time" placeholder="请选择时间" format="HH:mm" value-format="HH:mm" style="width: 100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="修肝时长">
                      <el-input v-model.number="statForm.trimming_duration" placeholder="请输入" style="width: 100%">
                         <template #append>min</template>
                      </el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="胆囊状态">
                       <el-select v-model="statForm.gallbladder_status" placeholder="请选择" style="width: 100%">
                          <el-option label="切除" value="切除" />
                          <el-option label="保留" value="保留" />
                       </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="6">
                    <el-form-item label="插管质量评分">
                      <el-rate v-model="statForm.cannulation_score" :max="5" show-score text-color="#ff9900" />
                    </el-form-item>
                  </el-col>
                   <el-col :span="6">
                    <el-button type="success" @click="submitStatInfo">
                      {{ editingStatId ? '保存修改' : '保存' }}
                    </el-button>
                    <el-button v-if="editingStatId" @click="resetStatForm" style="margin-left: 5px;">取消</el-button>
                  </el-col>
                  <el-col :span="24">
                    <el-form-item label="肝脏分叶情况">
                      <el-input v-model="statForm.liver_lobulation" type="textarea" placeholder="描述是否有解剖变异，如尾状叶肥大，影响血流分布" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>

              <el-divider content-position="left">已录入的统计信息</el-divider>
              <el-table 
                :data="currentExp.statistical_infos" 
                stripe 
                border 
                style="width: 100%" 
                height="300"
                :row-class-name="tableRowClassName"
              >
                <el-table-column prop="fasting_time" label="术前禁食(h)" width="120" />
                <el-table-column prop="anesthesia_method" label="麻醉方式" width="120" />
                <el-table-column prop="heparin_dosage" label="肝素化剂量(mg/kg)" width="150" />
                <el-table-column prop="acquisition_time" label="取肝时间" width="120" />
                <el-table-column prop="trimming_duration" label="修肝时长(min)" width="120" />
                <el-table-column prop="gallbladder_status" label="胆囊状态" width="100" />
                <el-table-column prop="cannulation_score" label="插管评分" width="100" />
                <el-table-column prop="liver_lobulation" label="肝脏分叶情况" min-width="200" show-overflow-tooltip />
                <el-table-column label="操作" width="120" fixed="right">
                  <template #default="scope">
                     <el-button link type="primary" size="small" @click="editStatInfo(scope.row)">编辑</el-button>
                     <el-popconfirm title="确定删除吗?" @confirm="deleteStatInfo(scope.row.id)">
                      <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="📷 多媒体资料 (Multimedia)">
              <el-tabs type="card">
                <el-tab-pane v-for="(label, key) in mediaTypes" :key="key" :label="label">
                  <div style="margin-bottom: 20px;">
                     <el-form :inline="true">
                       <el-form-item label="时间点 T=">
                         <el-input v-model="mediaForms[key].record_time" placeholder="请输入" style="width: 150px">
                           <template #append>h</template>
                         </el-input>
                       </el-form-item>
                       <el-form-item>
                         <el-upload
                           class="upload-demo"
                           action="#"
                           :auto-upload="false"
                           :on-change="(file) => handleFileChange(file, key)"
                           :show-file-list="false"
                         >
                           <el-button type="primary">选择文件</el-button>
                         </el-upload>
                       </el-form-item>
                       <el-form-item>
                          <span v-if="mediaForms[key].file" style="margin-right: 10px; color: #409EFF;">
                            {{ mediaForms[key].file.name }}
                          </span>
                       </el-form-item>
                       <el-form-item>
                         <el-button type="success" @click="submitMedia(key)" :disabled="!mediaForms[key].file || uploadingType === key">
                           {{ uploadingType === key ? '上传中...' : '上传' }}
                         </el-button>
                       </el-form-item>
                       <el-form-item v-if="uploadingType === key">
                         <el-progress 
                           :percentage="uploadProgress" 
                           :status="uploadProgress === 100 ? 'success' : ''"
                           style="width: 150px"
                         />
                       </el-form-item>
                     </el-form>
                  </div>
                  <el-divider content-position="left">已上传列表</el-divider>
                  <div class="media-grid">
                     <div v-for="item in getMediaList(key)" :key="item.id" class="media-item">
                       <!-- 图片显示 -->
                       <el-image 
                         v-if="['macro', 'infrared', 'pathology'].includes(key)"
                         style="width: 200px; height: 150px"
                         :src="getMediaUrl(item.file_path)"
                         :preview-src-list="[getMediaUrl(item.file_path)]"
                         fit="cover"
                       />
                       <!-- 视频显示 -->
                       <video 
                         v-else-if="key === 'video'" 
                         controls 
                         style="width: 200px; height: 150px; background: #000;"
                       >
                         <source :src="getMediaUrl(item.file_path)" type="video/mp4">
                         您的浏览器不支持视频标签。
                       </video>
                       
                       <div class="media-info">
                         <div class="time-tag">T={{ item.record_time }}h</div>
                         <div class="filename" :title="item.original_filename">{{ item.original_filename }}</div>
                         <el-popconfirm title="确定删除吗?" @confirm="deleteMedia(item.id)">
                            <template #reference>
                              <el-button type="danger" link size="small">删除</el-button>
                            </template>
                         </el-popconfirm>
                       </div>
                     </div>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-tab-pane>

            <el-tab-pane label="📝 专家记录 (Expert Records)">
              <div class="expert-section">
                <!-- 1. 专家主观描述 -->
                <el-card class="box-card" shadow="never" style="margin-bottom: 20px;">
                  <template #header>
                    <div class="card-header">
                      <span>👨‍⚕️ 专家主观描述</span>
                    </div>
                  </template>
                  <el-form :inline="true" :model="expertForm" class="demo-form-inline">
                    <el-form-item label="时间点 T=">
                      <el-input v-model="expertForm.record_time" placeholder="如 1" style="width: 100px">
                        <template #append>h</template>
                      </el-input>
                    </el-form-item>
                    <el-form-item label="描述">
                      <el-input 
                        v-model="expertForm.description" 
                        type="textarea" 
                        placeholder="请输入肝脏状态描述..." 
                        style="width: 400px"
                        :rows="2"
                      />
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="submitExpertDesc">添加记录</el-button>
                    </el-form-item>
                  </el-form>
                  
                  <el-table :data="currentExp.expert_descriptions" border stripe style="width: 100%" height="250">
                    <el-table-column prop="record_time" label="时间点 (h)" width="120">
                       <template #default="scope">T={{ scope.row.record_time }}</template>
                    </el-table-column>
                    <el-table-column prop="description" label="描述内容" />
                    <el-table-column label="操作" width="100">
                      <template #default="scope">
                        <el-popconfirm title="确定删除吗?" @confirm="deleteExpertDesc(scope.row.id)">
                          <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                        </el-popconfirm>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-card>

                <!-- 2. 干预与操作日志 -->
                <el-card class="box-card" shadow="never">
                  <template #header>
                    <div class="card-header">
                      <span>🛠️ 干预与操作日志</span>
                    </div>
                  </template>
                  <el-form :model="opLogForm" label-width="100px">
                    <el-row :gutter="20">
                      <el-col :span="12">
                        <el-form-item label="操作详情">
                          <el-input v-model="opLogForm.operation_details" type="textarea" :rows="3" placeholder="做了什么操作..." />
                        </el-form-item>
                      </el-col>
                      <el-col :span="12">
                        <el-form-item label="操作原因">
                          <el-input v-model="opLogForm.operation_reason" type="textarea" :rows="3" placeholder="为什么这么做..." />
                        </el-form-item>
                      </el-col>
                    </el-row>
                    <el-form-item>
                      <el-button type="primary" @click="submitOpLog">添加日志</el-button>
                    </el-form-item>
                  </el-form>

                  <el-table :data="currentExp.operation_logs" border stripe style="width: 100%" height="250">
                    <el-table-column prop="operation_details" label="操作详情" />
                    <el-table-column prop="operation_reason" label="操作原因" />
                    <el-table-column label="操作" width="100">
                      <template #default="scope">
                        <el-popconfirm title="确定删除吗?" @confirm="deleteOpLog(scope.row.id)">
                          <template #reference><el-button link type="danger" size="small">删除</el-button></template>
                        </el-popconfirm>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-card>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
    </div>

    <!-- 灌注数据查看弹窗 -->
    <el-dialog v-model="viewDialogVisible" :title="'文件数据详情: ' + viewingFileName" width="80%">
      <el-table :data="viewDialogData" stripe border height="500">
         <el-table-column prop="record_time" label="灌注时间" width="180" />
         <el-table-column prop="pv_pressure" label="PV压力(mmHg)" />
         <el-table-column prop="pv_flow" label="PV流量(ml/min)" />
         <el-table-column prop="ha_pressure" label="HA压力(mmHg)" />
         <el-table-column prop="ha_flow" label="HA流量(ml/min)" />
         <el-table-column prop="temperature" label="温度(℃)" />
      </el-table>
    </el-dialog>
  </el-config-provider>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox, ElConfigProvider } from 'element-plus' // [修改] 引入 ConfigProvider
import zhCn from 'element-plus/es/locale/lang/zh-cn' // [新增] 引入中文包
import { UploadFilled } from '@element-plus/icons-vue'

const expCode = ref('NMP-Pig-001') 
const currentExp = ref(null)
const loadingExp = ref(false)
const showExpSelector = ref(false)
const allExperiments = ref([])

const openExperimentSelector = async () => {
  try {
    const res = await axios.get('/experiments/')
    allExperiments.value = res.data
    showExpSelector.value = true
  } catch (error) {
    ElMessage.error('获取实验列表失败')
  }
}

const selectExperiment = (row) => {
  expCode.value = row.experiment_code
  showExpSelector.value = false
  confirmExperiment()
}

const formatDate = (row, column, cellValue) => {
  if (!cellValue) return ''
  return new Date(cellValue).toLocaleString()
}

const editingBasicId = ref(null)
const editingBgId = ref(null)
const editingBioId = ref(null)
const editingStatId = ref(null)

const bgForm = reactive({
  record_time: '',
  sample_site: '',
  ph: undefined,
  pco2: undefined,
  po2: undefined,
  na: undefined,
  k: undefined,
  cl: undefined,
  ca: undefined,
  glu: undefined,
  lac: undefined,
  hct: undefined,
  tco2: undefined,
  hb: undefined,
  hco3: undefined,
  be_ecf: undefined,
  be_b: undefined,
  so2: undefined,
  an_gap: undefined
})
const bioForm = reactive({
  record_time: '',
  sample_site: '',
  sample_source: 'OnSite',
  alt: undefined,
  ast: undefined,
  alb: undefined,
  tp: undefined,
  dbil: undefined,
  tbil: undefined,
  glob: undefined,
  ag_ratio: undefined,
  crea: undefined,
  ua: undefined,
  tg: undefined,
  tc: undefined,
  hdl: undefined,
  glu: undefined,
  urea: undefined,
  urea_crea_ratio: undefined,
  ldl: undefined
})
const statForm = reactive({
  fasting_time: undefined,
  anesthesia_method: '',
  heparin_dosage: undefined,
  acquisition_time: '',
  trimming_duration: undefined,
  liver_lobulation: '',
  gallbladder_status: '',
  cannulation_score: undefined
})
const basicForm = reactive({
  record_date: '',
  donor_breed: '',
  gender: '',
  age_months: undefined,
  weight_kg: undefined,
  total_duration: undefined,
  total_bile: undefined,
  liver_weight_pre: undefined,
  liver_weight_post: undefined,
  cold_ischemia_time: undefined,
  warm_ischemia_time: undefined,
  perfusion_liquid_vol: undefined
})

const confirmExperiment = async () => {
  if(!expCode.value) return ElMessage.warning('请输入编号')
  loadingExp.value = true

  try {
    const res = await axios.get(`/experiments/${expCode.value}`)
    currentExp.value = res.data
    ElMessage.success(`查询成功：${res.data.experiment_code}`)
  } catch (error) {
    if (error.response && error.response.status === 404) {
      ElMessageBox.confirm(`实验编号 "${expCode.value}" 不存在。是否立即新建？`, '提示', {
        confirmButtonText: '是的，新建',
        cancelButtonText: '取消',
        type: 'warning',
      }).then(async () => {
        try {
          const createRes = await axios.post('/experiments/', { experiment_code: expCode.value })
          currentExp.value = createRes.data
          ElMessage.success('新建成功！')
        } catch (e) { ElMessage.error('创建失败') }
      }).catch(() => { ElMessage.info('已取消') })
    } else {
      ElMessage.error('连接服务器失败')
    }
  } finally {
    loadingExp.value = false
  }
}

const refreshData = async () => {
  if(!currentExp.value) return
  try {
    const res = await axios.get(`/experiments/${currentExp.value.experiment_code}`)
    currentExp.value = res.data
  } catch (e) { console.error(e) }
}

const submitBasicInfo = async () => {
  try {
    if (editingBasicId.value) {
      // Update existing
      await axios.put(`/basic-info/${editingBasicId.value}`, {
        experiment_id: currentExp.value.id,
        ...basicForm
      })
      ElMessage.success('基本信息已更新')
    } else {
      // Create new
      await axios.post('/basic-info/', {
        experiment_id: currentExp.value.id,
        ...basicForm
      })
      ElMessage.success('基本信息已保存')
    }
    refreshData()
    resetBasicForm()
  } catch (e) { ElMessage.error('保存失败') }
}

const editBasicInfo = (row) => {
  editingBasicId.value = row.id
  Object.assign(basicForm, {
    record_date: row.record_date,
    donor_breed: row.donor_breed,
    gender: row.gender,
    age_months: row.age_months,
    weight_kg: row.weight_kg,
    total_duration: row.total_duration,
    total_bile: row.total_bile,
    liver_weight_pre: row.liver_weight_pre,
    liver_weight_post: row.liver_weight_post,
    cold_ischemia_time: row.cold_ischemia_time,
    warm_ischemia_time: row.warm_ischemia_time,
    perfusion_liquid_vol: row.perfusion_liquid_vol
  })
}

const resetBasicForm = () => {
  editingBasicId.value = null
  Object.assign(basicForm, {
    record_date: '',
    donor_breed: '',
    gender: '',
    age_months: undefined,
    weight_kg: undefined,
    total_duration: undefined,
    total_bile: undefined,
    liver_weight_pre: undefined,
    liver_weight_post: undefined,
    cold_ischemia_time: undefined,
    warm_ischemia_time: undefined,
    perfusion_liquid_vol: undefined
  })
}

const deleteBasicInfo = async (id) => {
  try { await axios.delete(`/basic-info/${id}`); ElMessage.success('已删除'); refreshData() } catch (e) { ElMessage.error('删除失败') }
}

const submitBloodGas = async () => {
  try {
    if (editingBgId.value) {
      await axios.put(`/bloodgas/${editingBgId.value}`, { experiment_id: currentExp.value.id, ...bgForm })
      ElMessage.success('更新成功')
    } else {
      await axios.post('/bloodgas/', { experiment_id: currentExp.value.id, ...bgForm })
      ElMessage.success('保存成功')
    }
    refreshData()
    resetBgForm()
  } catch (e) { ElMessage.error('保存失败') }
}

const editBloodGas = (row) => {
  editingBgId.value = row.id
  Object.assign(bgForm, {
    record_time: row.record_time,
    sample_site: row.sample_site,
    ph: row.ph,
    pco2: row.pco2,
    po2: row.po2,
    na: row.na,
    k: row.k,
    cl: row.cl,
    ca: row.ca,
    glu: row.glu,
    lac: row.lac,
    hct: row.hct,
    tco2: row.tco2,
    hb: row.hb,
    hco3: row.hco3,
    be_ecf: row.be_ecf,
    be_b: row.be_b,
    so2: row.so2,
    an_gap: row.an_gap
  })
}

const resetBgForm = () => {
  editingBgId.value = null
  Object.assign(bgForm, {
    record_time: '',
    sample_site: '',
    ph: undefined,
    pco2: undefined,
    po2: undefined,
    na: undefined,
    k: undefined,
    cl: undefined,
    ca: undefined,
    glu: undefined,
    lac: undefined,
    hct: undefined,
    tco2: undefined,
    hb: undefined,
    hco3: undefined,
    be_ecf: undefined,
    be_b: undefined,
    so2: undefined,
    an_gap: undefined
  })
}

const submitBiochem = async () => {
  try {
    if (editingBioId.value) {
      await axios.put(`/biochem/${editingBioId.value}`, { experiment_id: currentExp.value.id, ...bioForm })
      ElMessage.success('更新成功')
    } else {
      await axios.post('/biochem/', { experiment_id: currentExp.value.id, ...bioForm })
      ElMessage.success('保存成功')
    }
    refreshData()
    resetBioForm()
  } catch (e) { ElMessage.error('保存失败') }
}

const editBiochem = (row) => {
  editingBioId.value = row.id
  Object.assign(bioForm, {
    record_time: row.record_time,
    sample_site: row.sample_site,
    sample_source: row.sample_source,
    alt: row.alt,
    ast: row.ast,
    alb: row.alb,
    tp: row.tp,
    dbil: row.dbil,
    tbil: row.tbil,
    glob: row.glob,
    ag_ratio: row.ag_ratio,
    crea: row.crea,
    ua: row.ua,
    tg: row.tg,
    tc: row.tc,
    hdl: row.hdl,
    glu: row.glu,
    urea: row.urea,
    urea_crea_ratio: row.urea_crea_ratio,
    ldl: row.ldl
  })
}

const resetBioForm = () => {
  editingBioId.value = null
  Object.assign(bioForm, {
    record_time: '',
    sample_site: '',
    sample_source: 'OnSite',
    alt: undefined,
    ast: undefined,
    alb: undefined,
    tp: undefined,
    dbil: undefined,
    tbil: undefined,
    glob: undefined,
    ag_ratio: undefined,
    crea: undefined,
    ua: undefined,
    tg: undefined,
    tc: undefined,
    hdl: undefined,
    glu: undefined,
    urea: undefined,
    urea_crea_ratio: undefined,
    ldl: undefined
  })
}

const submitStatInfo = async () => {
  try {
    if (editingStatId.value) {
      await axios.put(`/statistical-info/${editingStatId.value}`, {
        experiment_id: currentExp.value.id,
        ...statForm
      })
      ElMessage.success('统计信息已更新')
    } else {
      await axios.post('/statistical-info/', {
        experiment_id: currentExp.value.id,
        ...statForm
      })
      ElMessage.success('统计信息已保存')
    }
    refreshData()
    resetStatForm()
  } catch (e) { ElMessage.error('保存失败') }
}

const editStatInfo = (row) => {
  editingStatId.value = row.id
  Object.assign(statForm, {
    fasting_time: row.fasting_time,
    anesthesia_method: row.anesthesia_method,
    heparin_dosage: row.heparin_dosage,
    acquisition_time: row.acquisition_time,
    trimming_duration: row.trimming_duration,
    liver_lobulation: row.liver_lobulation,
    gallbladder_status: row.gallbladder_status,
    cannulation_score: row.cannulation_score
  })
}

const resetStatForm = () => {
  editingStatId.value = null
  Object.assign(statForm, {
    fasting_time: undefined,
    anesthesia_method: '',
    heparin_dosage: undefined,
    acquisition_time: '',
    trimming_duration: undefined,
    liver_lobulation: '',
    gallbladder_status: '',
    cannulation_score: undefined
  })
}

const deleteStatInfo = async (id) => {
  try { await axios.delete(`/statistical-info/${id}`); ElMessage.success('已删除'); refreshData() } catch (e) { ElMessage.error('删除失败') }
}

const deleteBloodGas = async (id) => {
  try { await axios.delete(`/bloodgas/${id}`); ElMessage.success('已删除'); refreshData() } catch (e) { ElMessage.error('删除失败') }
}

const deleteBiochem = async (id) => {
  try { await axios.delete(`/biochem/${id}`); ElMessage.success('已删除'); refreshData() } catch (e) { ElMessage.error('删除失败') }
}

const uploadPerfusionFile = async (options) => {
  if (!currentExp.value) return ElMessage.warning('请先查询或创建实验')
  
  const formData = new FormData()
  formData.append('file', options.file)
  
  try {
    const res = await axios.post(`/experiments/${currentExp.value.id}/perfusion-machine-data/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    ElMessage.success(res.data.message || '上传成功')
    refreshData()
  } catch (error) {
    ElMessage.error('上传失败: ' + (error.response?.data?.detail || error.message))
  }
}

// --- 灌注物理参数文件管理 ---
const viewDialogVisible = ref(false)
const viewDialogData = ref([])
const viewingFileName = ref('')

const deletePerfusionFile = async (id) => {
  try {
    await axios.delete(`/perfusion-files/${id}`)
    ElMessage.success('已删除')
    refreshData()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

const viewPerfusionFile = async (row) => {
    viewingFileName.value = row.filename
    try {
        const res = await axios.get(`/perfusion-files/${row.id}/data`)
        viewDialogData.value = res.data
        viewDialogVisible.value = true
    } catch(e) { ElMessage.error('获取数据失败') }
}

const downloadPerfusionJson = async (row) => {
  try {
    const res = await axios.get(`/perfusion-files/${row.id}/json`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${row.filename}.json`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch(e) { ElMessage.error('下载失败') }
}

const tableRowClassName = ({ row }) => {
  if (row.id === editingBasicId.value || row.id === editingBgId.value || row.id === editingBioId.value || row.id === editingStatId.value) {
    return 'editing-row'
  }
  return ''
}

// --- 多媒体相关逻辑 ---
const mediaTypes = {
  macro: '宏观外观图像',
  infrared: '红外热成像',
  video: '视频片段',
  pathology: '病理图像'
}

const mediaForms = reactive({
  macro: { record_time: '', file: null },
  infrared: { record_time: '', file: null },
  video: { record_time: '', file: null },
  pathology: { record_time: '', file: null }
})

const handleFileChange = (file, type) => {
  mediaForms[type].file = file.raw
}

const uploadProgress = ref(0)
const uploadingType = ref(null)

const submitMedia = async (type) => {
  if (!mediaForms[type].record_time) return ElMessage.warning('请输入时间点')
  if (!mediaForms[type].file) return ElMessage.warning('请选择文件')
  
  const formData = new FormData()
  formData.append('file', mediaForms[type].file)
  formData.append('file_type', type)
  formData.append('record_time', mediaForms[type].record_time)
  
  uploadingType.value = type
  uploadProgress.value = 0
  
  try {
    await axios.post(`/experiments/${currentExp.value.id}/media/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    })
    ElMessage.success('上传成功')
    mediaForms[type].file = null
    mediaForms[type].record_time = ''
    refreshData()
  } catch (e) {
    ElMessage.error('上传失败')
  } finally {
    setTimeout(() => {
      uploadingType.value = null
      uploadProgress.value = 0
    }, 1000)
  }
}

const getMediaList = (type) => {
  if (!currentExp.value || !currentExp.value.medias) return []
  return currentExp.value.medias.filter(m => m.file_type === type)
}

const getMediaUrl = (path) => {
  return `/media/${path}`
}

const deleteMedia = async (id) => {
  try {
    await axios.delete(`/media-records/${id}`)
    ElMessage.success('删除成功')
    refreshData()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

// --- 专家记录相关逻辑 ---
const expertForm = reactive({
  record_time: '',
  description: ''
})

const opLogForm = reactive({
  operation_details: '',
  operation_reason: ''
})

const submitExpertDesc = async () => {
  if (!expertForm.record_time || !expertForm.description) return ElMessage.warning('请填写完整信息')
  try {
    await axios.post(`/experiments/${currentExp.value.id}/expert-descriptions`, {
      experiment_id: currentExp.value.id,
      ...expertForm
    })
    ElMessage.success('添加成功')
    expertForm.record_time = ''
    expertForm.description = ''
    refreshData()
  } catch (e) { ElMessage.error('添加失败') }
}

const deleteExpertDesc = async (id) => {
  try { await axios.delete(`/expert-descriptions/${id}`); ElMessage.success('已删除'); refreshData() } catch (e) { ElMessage.error('删除失败') }
}

const submitOpLog = async () => {
  if (!opLogForm.operation_details || !opLogForm.operation_reason) return ElMessage.warning('请填写完整日志')
  try {
    await axios.post(`/experiments/${currentExp.value.id}/operation-logs`, {
      experiment_id: currentExp.value.id,
      ...opLogForm
    })
    ElMessage.success('添加成功')
    opLogForm.operation_details = ''
    opLogForm.operation_reason = ''
    refreshData()
  } catch (e) { ElMessage.error('添加失败') }
}

const deleteOpLog = async (id) => {
  try { await axios.delete(`/operation-logs/${id}`); ElMessage.success('已删除'); refreshData() } catch (e) { ElMessage.error('删除失败') }
}
</script>

<style>
/* 全局样式或不加 scoped 才能生效到 el-table 的 row 上 */
.el-table .editing-row {
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
  border: 2px solid var(--el-color-warning) !important;
}
.el-table .editing-row td.el-table__cell {
    background-color: var(--el-color-warning-light-9) !important;
}
</style>

<style scoped>
/* 1. 容器：强制占满屏幕高度，不许出现外层滚动条 */
.app-container { 
  padding: 20px; 
  display: flex; 
  justify-content: center; 
  background: #f5f7fa; 
  height: 100vh; /* 关键：100vh 表示 100% 屏幕高度 */
  overflow: hidden; /* 关键：超出屏幕的内容隐藏，防止双重滚动条 */
  box-sizing: border-box;
}

/* 2. 卡片：占满容器的宽高，并使用 Flex 布局管理内部 */
.box-card { 
  width: 100%;       /* 宽度铺满 */
  height: 100%;      /* 高度铺满 */
  display: flex;     /* 开启 Flex 布局 */
  flex-direction: column; /* 垂直排列：头部在上，内容在下 */
} 

/* 3. 卡片头部：保持不动 */
:deep(.el-card__header) {
  flex-shrink: 0; /* 禁止压缩头部 */
}

/* 4. 卡片主体内容：自动填充剩余高度，并允许内部滚动 */
:deep(.el-card__body) {
  flex: 1;            /* 占据剩余的所有空间 */
  overflow-y: auto;   /* 关键：内容太多时，只在卡片内部出现滚动条 */
  display: flex;
  flex-direction: column;
}

.input-area { 
  background: #fafafa; 
  padding: 15px; 
  border-radius: 8px; 
  margin-bottom: 20px; 
}

/* 5. 修复 Tabs 也可以撑开高度 (可选，视情况而定) */
:deep(.el-tabs) {
  flex: 1;
  display: flex;
  flex-direction: column;
}
:deep(.el-tabs__content) {
  flex: 1;
  overflow-y: auto; /* 如果想让 Tab 内容独立滚动，可以加这个 */
}

/* 多媒体网格布局 */
.media-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.media-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.media-info {
  margin-top: 10px;
  width: 100%;
  text-align: center;
}

.time-tag {
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.filename {
  font-size: 12px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
  margin-bottom: 5px;
}
</style>
